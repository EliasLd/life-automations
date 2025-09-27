# Automated System Update Script for Arch Linux

## Overview

This Python script automates system updates for Arch Linux. It checks for available updates in both the official repositories (using `pacman`) and the AUR (using `yay`). If updates are found, it can install them automatically and notify the user about the update status through desktop notifications.

## Features

- **Checks for Updates:** Scans both official repositories and the AUR for pending package updates.
- **Automated Installation:** Installs available updates automatically if configured.
- **Desktop Notifications:** Sends notifications about available updates and installation results.
- **Logging:** All update events and results are recorded in a local log file for future reference.

## Log File Location

You can access the update log at:
```
~/.local/share/system-update.log
```
This file contains a timestamped record of update checks, installations, and any errors encountered.

## Disclaimer: Passwordless Sudo for Pacman

This script requires passwordless sudo privileges for the `pacman` command to perform automated updates without user intervention.  
**Granting passwordless sudo access to pacman can have security implications**—ensure you understand the risks before enabling this feature.  
You can configure this by adding the following line to your sudoers file (using `visudo`):

```
your_username ALL=(ALL) NOPASSWD: /usr/bin/pacman
```

Replace `your_username` with your actual username.

## Usage

Configure the script to run on startup (for example, using a systemd user service or timer), or run it manually as needed.  
Make sure your notification daemon (e.g., dunst) is running to receive desktop notifications.

---
