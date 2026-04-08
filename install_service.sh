#!/bin/bash
# Install SALENE systemd service
# Run with sudo

set -e

echo "Installing SALENE daemon service..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo ./install_service.sh"
    exit 1
fi

# Copy service file
cp salene-daemon.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable service (start on boot)
systemctl enable salene-daemon.service

echo "✅ Service installed and enabled"
echo ""
echo "Commands:"
echo "  sudo systemctl start salene-daemon    # Start now"
echo "  sudo systemctl stop salene-daemon     # Stop"
echo "  sudo systemctl status salene-daemon   # Check status"
echo "  sudo systemctl disable salene-daemon  # Disable auto-start"
echo ""
echo "Logs:"
echo "  sudo journalctl -u salene-daemon -f   # Follow logs"
echo "  sudo journalctl -u salene-daemon --since '1 hour ago'"
