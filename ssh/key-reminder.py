import os
import pathlib
import time
import subprocess

# CONFIGURABLES
SSH_DIR = os.path.expanduser("~/.ssh")
LOG_DIR = os.path.expanduser("~/.local/share")
LOG_FILE = os.path.join(LOG_DIR, "ssh-key-reminder.log")
THRESHOLD_DAYS = 180 # Notify if key is older than this

def log(line):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{ts} {line}\n")

