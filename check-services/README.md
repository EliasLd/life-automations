# Service Health Check Script

## Overview

This Go script checks the health of multiple personal services by sending HTTP requests to specified endpoints and verifying the expected responses.  
It's designed to run automatically (e.g., at startup via systemd) and logs results to a file, while sending a desktop notification summarizing service statuses.

## Features

- Checks each service using a user-provided configuration file.
- Logs detailed results and status summaries to `~/.local/share/service-check.log`.
- Sends a desktop notification summarizing which services are up or down.
- Command-line interface for explicit configuration file selection.

## Usage

### 1. Build the Script

In the `check-services` directory, run:

```sh
go build -o check_services
```
Or install system-wide (if desired):

```sh
go install
```

### 2. Prepare Your Configuration File

Create a JSON file describing each service to check.  
Example `services.json`:

```json
[
    {
        "name": "Personal Website",
        "url": "https://eliasld.com",
        "expected": "<!DOCTYPE html>"
    },
    {
        "name": "Backend Health",
        "url": "http://<public_ip_address>:8080/health",
        "expected": "Server is healthy !"
    }
]
```

**Each object must have:**
- `name`: a unique, human-readable identifier for the service.
- `url`: the endpoint to query (e.g., home page for a website, `/health` for an API).
- `expected`: a string that should be present in the response to consider the service healthy.

### 3. Run the Script

You must provide the path to your configuration file as the first argument:

```sh
./check_services /path/to/services.json
```

### 4. Log File

All service check results and status summaries are logged to:

```
~/.local/share/service-check.log
```

### 5. Desktop Notifications

A desktop notification (using `notify-send`) will show a summary after each run.  
Make sure you have a notification daemon running (e.g., `dunst`).

### 6. Automate with systemd (optional)

You can use a systemd user service and timer to run this script automatically at boot or intervals.  
See the main project documentation for an example.

## Disclaimer

- The script will fail if the configuration file is missing or invalid.
- Requires network connectivity to reach each service endpoint.
- The script checks for the presence of the expected string in the HTTP response; for more advanced checks, modify the script accordingly.

---
