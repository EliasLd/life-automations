#!/usr/bin/env python3

import subprocess
import datetime
from pathlib import Path

LOG_FILE = Path.home() / ".local/share/system-update.log"

def run(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

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

def auto_update_pacman():
    result = run("sudo pacman -Syu --noconfirm")
    log("Official repo update:\n" + result.stdout + result.stderr)
    if result.returncode != 0:
        notify("System update error", "Pacman update failed!")
        log("Pacman update failed.")
    else:
        notify("System Update", "All pacman updates installed automatically!")


def auto_update_aur():
    result = run("yay -Syu --noconfirm")
    log("AUR update:\n" + result.stdout + result.stderr)
    if result.returncode != 0:
        notify("System Update Error", "AUR update failed!")
    else:
        notify("System Update", "All AUR updates installed automatically!")


def main():
    pacman_updates = check_pacman_updates()
    aur_updates = check_aur_updates()
    total_updates = len(pacman_updates) + len(aur_updates)

    if total_updates == 0:
        notify("System Update", "No updates available 🎉")
        log("No updates available.")
        return

    update_msg = f"{len(pacman_updates)} official + {len(aur_updates)} AUR update(s) available."
    notify("System Update", update_msg)
    log(update_msg)

    if len(pacman_updates) > 0:
        auto_update_pacman()

    if len(aur_updates) > 0:
        auto_update_aur()

if __name__ == "__main__":
    main()
