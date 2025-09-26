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
