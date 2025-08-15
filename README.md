
# Time-Caboodle

Time-Caboodle is a project for building a cluster of homemade NTP (Network Time Protocol) appliances. It is designed for experimentation and learning about time synchronization using GPS and custom hardware.

## Features
- GPS-based time synchronization
- Custom display for time output
- Modular Python codebase
- Systemd integration for service management

## Directory Structure

- `code/` — Python scripts for time, GPS, and display logic
- `conf/` — Configuration files (e.g., NTP)
- `sysmod/` — Systemd service and udev rules

## Installation

### System Dependencies

```bash
sudo apt update
sudo apt install python3-pip fonts-dejavu python3-pil python3-numpy
```

### Python Dependencies

```bash
pip3 install --upgrade setuptools
pip3 install adafruit-circuitpython-rgb-display
pip3 install --upgrade --force-reinstall spidev
pip3 install gpsdclient
```

## Usage

1. Connect your GPS hardware and display.
2. Configure NTP and systemd services as needed (see `conf/` and `sysmod/`).
3. Run the main Python scripts in `code/` to start the time display and synchronization.

## License

See `LICENSE` for details.
