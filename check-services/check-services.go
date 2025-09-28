package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

type Site struct {
	Name     string `json:"name"`
	URL      string `json:"url"`
	Expected string `json:"expected"`
}
