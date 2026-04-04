# Shiki Dashboard

Lightweight administration dashboard for monitoring SMART-enabled drives, service uptime, and host system health. It ships as a single Flask app with a canvas-style front end plus a small SQLite store so it can run on a private network without extra services.

## Features
- **Drive health & SMART telemetry** – uses `smartctl` (or mock data on macOS) to capture temperature, capacity, serial, and SMART attributes, stores a rolling history for each drive, and exposes `/api/drives`, `/api/drives/summary`, and `/api/drives/cached` for the UI.
- **Service monitoring** – define services with external and optional local checks (HTTP, HTTPS, TCP, ping); background threads keep service history updated, and you can reorder, edit, or trigger checks via `/api/services` endpoints.
- **System stats** – `psutil` snapshots are sampled in a background thread and returned through `/api/system-stats` so the UI can show CPU, memory, and bandwidth usage when `psutil` is installed.
- **Remote host monitoring** – run `remote_host_agent.py` on other LAN machines, register them in the new Hosts tab, and Shiki Dashboard will poll/store live CPU, RAM, and network samples with 1-minute charts and 1-hour retention.
- **Custom branding** – upload/crop an app logo via `/api/app-logo` and persist it in `app_settings`.

## Requirements & dependencies
- `pip install flask requests psutil`
- `python run.py`


## Quick start
1. `python -m venv venv && source venv/bin/activate`
2. `pip install flask requests psutil`
3. `python run.py`
4. Visit `http://localhost:8080` in your browser. The app will print the same URL on startup and poll drives/services in the background.

## Remote host agent
1. On the machine you want to monitor: `pip install flask psutil`
2. Run `python3 remote_host_agent.py --port 8765`
3. Optionally add `--token your-shared-token`
4. In the dashboard Hosts tab, add that machine's LAN IP, port, and token

## TODO
- Add if someone is watching on Emby
- NAS disk space stats
- TV shows / movies file size
- Integrate or fork off RealDebridClient

## Bug fix list
- Better padding on bottom nav for mobile
- Saving services requires the service to respond before leaving the add service screen
