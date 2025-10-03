import os
import pathlib
import time
import subprocess

# CONFIGURABLES
SSH_DIR = os.path.expanduser("~/.ssh")
LOG_DIR = os.path.expanduser("~/.local/share")
LOG_FILE = os.path.join(LOG_DIR, "ssh-key-reminder.log")
THRESHOLD_DAYS = 180 # Notify if key is older than this
