# Browser-Py: Proxy-Based Ad-Blocking Browser

A Python-based browser system with a server/client architecture featuring ad-blocking capabilities. The server acts as a proxy that can run as a systemd service on Raspberry Pi 5.

## Architecture

### Server (`server.py`)
- HTTP proxy server that runs as a service
- Serves ad-blocking JavaScript via REST API
- Can run 24/7 on headless systems
- Supports systemd service on Raspberry Pi

### Client (`client.py`)
- Desktop GUI browser using PyWebView
- Connects to the proxy server for ad-blocking
- Lightweight and can run on any system with a display

### Original (`browser.py`)
- Standalone browser with integrated ad-blocking
- No server required
- Works on systems with display capabilities

## Features

✨ **Ad-Blocking**: Removes ads while preserving site functionality  
🔄 **Navigation**: Back, forward, and reload buttons  
🌐 **URL Bar**: Direct URL input with automatic https:// prefix  
📡 **Proxy Mode**: Server/client architecture for remote browsing  
🍓 **Pi-Ready**: Easy deployment on Raspberry Pi 5 via systemd

## Quick Start

### Standalone Mode (Original)
```bash
python3 browser.py --url https://www.example.com
```

### Proxy Server Mode
```bash
# Terminal 1: Start the server
python3 server.py --host 0.0.0.0 --port 8080

# Terminal 2: Start the client
python3 client.py --url https://www.example.com --proxy http://localhost:8080
```

### Raspberry Pi 5 Service
See [SETUP_PI.md](SETUP_PI.md) for detailed installation instructions.

## Installation

### Requirements
- Python 3.8+
- tkinter (usually included with Python)
- PyWebView
- requests (for client)

### Setup
```bash
pip install -r requirements.txt
```

### System Dependencies (Ubuntu/Debian/Pi OS)
```bash
sudo apt-get install python3-tk python3-dev libgtk-3-dev libwebkit2gtk-4.0-dev
```

## API Endpoints (Server)

### `/` (GET)
Returns the server status page

### `/api/adblock` (GET)
Returns the ad-blocking JavaScript

### `/api/status` (GET)
Returns server status as JSON

Example:
```bash
curl http://localhost:8080/api/status
```

## Usage Examples

### Run server on specific port
```bash
python3 server.py --port 9000
```

### Connect client to remote server
```bash
python3 client.py --proxy http://192.168.1.100:8080
```

### Enable systemd service (Pi)
```bash
sudo systemctl enable browser-proxy.service
sudo systemctl start browser-proxy.service
```

## How Ad-Blocking Works

The system injects JavaScript that:
1. Removes known ad container selectors (iframes, divs with ad-related classes)
2. Uses regex patterns to identify ad-related elements by ID/class
3. Continuously monitors DOM changes to block dynamically-loaded ads
4. Preserves legitimate site functionality

## Troubleshooting

### Module not found errors
```bash
pip3 install --upgrade -r requirements.txt
```

### WebKit issues on Linux
```bash
sudo apt-get install libwebkit2gtk-4.0-dev
```

### Service won't start on Pi
```bash
sudo journalctl -u browser-proxy.service -n 50
```

## Performance

- **Server**: Lightweight HTTP server, ~10-30MB RAM usage
- **Client**: GUI application, ~100-150MB RAM usage
- **Pi 5**: Runs smoothly as a service with 4GB+ RAM

## License

See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit pull requests.