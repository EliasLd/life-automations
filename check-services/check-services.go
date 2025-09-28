package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

type Site struct {
	Name     string `json:"name"`
	URL      string `json:"url"`
	Expected string `json:"expected"`
}

func main() {
	var configFile string
	if len(os.Args) < 2 {
		fmt.Println("Usage: check-services <config.json>")
		fmt.Println("	<config.json>: Path to your JSON configuration file.")
		os.Exit(1)
	}
	configFile = os.Args[1]

	logDir := filepath.Join(os.Getenv("HOME"), ".local", "share")
	logFile := filepath.Join(logDir, "check-services.log")

	if err := os.MkdirAll(logDir, 0755); err != nil {
		fmt.Fprintf(os.Stderr, "Could not create log directory: %v\n", err)
		os.Exit(1)
	}

	f, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Could not open log file: %v\n", err)
		os.Exit(1)
	}
	defer f.Close()

	// Helper for logging with timestamp
	log := func(line string) {
		ts := time.Now().Format("[2006-01-02 15:04:05]")
		fmt.Fprintf(f, "%s %s\n", ts, line)
	}
	data, err := os.ReadFile(configFile)
	if err != nil {
		log(fmt.Sprintf("Error reading config file: %v", err))
		return
	}

	var sites []Site
	err = json.Unmarshal(data, &sites)
	if err != nil {
		log(fmt.Sprintf("Error parsing JSON: %v", err))
		return
	}

	var okList, failList []string

	for _, site := range sites {
		resp, err := http.Get(site.URL)
		if err != nil {
			failList = append(failList, site.Name)
			log(fmt.Sprintf("[FAIL] %s (%s): HTTP error: %v", site.Name, site.URL, err))
			continue
		}
		defer resp.Body.Close()

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			failList = append(failList, site.Name)
			log(fmt.Sprintf("[FAIL] %s (%s) Error reading response: %v", site.Name, site.URL, err))
			continue
		}

		content := string(body)
		if strings.Contains(content, site.Expected) {
			okList = append(okList, site.Name)
			log(fmt.Sprintf("[OK] %s (%s): Response matches expected.", site.Name, site.URL))
		} else {
			failList = append(failList, site.Name)
			log(fmt.Sprintf("[FAIL] %s (%s): Response does not match expected.", site.Name, site.URL))
		}
	}

	// Build notification summary
	var summary strings.Builder
	if len(okList) > 0 {
		summary.WriteString("Working: " + strings.Join(okList, ", ") + "\n")
	} else {
		summary.WriteString("Working: None\n")
	}
	if len(failList) > 0 {
		summary.WriteString("Failing: " + strings.Join(failList, ", "))
	} else {
		summary.WriteString("Failing: None 🎉")
	}

	// Log the summary
	log("Summary: " + strings.ReplaceAll(summary.String(), "\n", " | "))

	// Send desktop notification of the summary
	exec.Command("notify-send", "Service Status", summary.String()).Run()
}
