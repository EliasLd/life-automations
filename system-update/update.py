#!/usr/bin/env python3

import subprocess
import datetime
import os
from pathlib import Path

LOG_FILE = Path.home() / ".local/share/system-update.log"

def run(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)

def notify(title, message):
    run(f'notify-send "{title}" "{message}"')

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] - {message}\n")

def check_pacman_updates():
    result = run("checkupdates")
    packages = result.stdout.strip().split("\n") if result.stdout else []
    return packages

def check_aur_updates():
    result = run("yay -Qu")
    packages = result.stdout.strip().split("\n") if result.stdout else []
    return packages

def main():
    pacman_updates = check_pacman_updates()
    aur_updates = check_aur_updates()
    total_updates = len(pacman_updates) + len(aur_updates)

    if total_updates == 0:
        notify("System Update", "No updates available 🎉")
        log("No updates available.")
        return

    update_msg = f"{len(pacman_updates)} official + {len(aur_updates)} AUR updates availble."
    notify("System Update", update_msg)
    log(update_msg)

if __name__ == "__main__":
    main()
