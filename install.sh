#!/bin/bash
#
# Timelapse Menu Bar - Installer
# This script installs the app and sets it to run automatically on login.
#

set -e

echo "=================================="
echo "  Timelapse Menu Bar - Installer"
echo "=================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="timelapse-menubar"
PLIST_NAME="com.timelapse-menubar.plist"
LAUNCHAGENT_DIR="$HOME/Library/LaunchAgents"

# Check for Python 3
echo "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "ERROR: Python 3 is not installed."
    echo ""
    echo "Please install Python 3 first:"
    echo "  1. Visit https://www.python.org/downloads/"
    echo "  2. Download and install the latest Python 3"
    echo "  3. Run this installer again"
    echo ""
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "  Found $PYTHON_VERSION"

# Check for ffmpeg
echo ""
echo "Checking for ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "ERROR: ffmpeg is not installed."
    echo ""
    echo "Please install ffmpeg first. The easiest way is with Homebrew:"
    echo ""
    echo "  1. Install Homebrew (if you don't have it):"
    echo "     /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo ""
    echo "  2. Install ffmpeg:"
    echo "     brew install ffmpeg"
    echo ""
    echo "  3. Run this installer again"
    echo ""
    exit 1
fi
FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -1)
echo "  Found $FFMPEG_VERSION"

# Create virtual environment
echo ""
echo "Setting up Python environment..."
cd "$SCRIPT_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Created virtual environment"
else
    echo "  Virtual environment already exists"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "  Dependencies installed"

# Stop existing instance if running
echo ""
echo "Configuring auto-start..."
if launchctl list | grep -q "$PLIST_NAME" 2>/dev/null; then
    launchctl unload "$LAUNCHAGENT_DIR/$PLIST_NAME" 2>/dev/null || true
fi

# Create LaunchAgent plist
mkdir -p "$LAUNCHAGENT_DIR"
cat > "$LAUNCHAGENT_DIR/$PLIST_NAME" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$PLIST_NAME</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/venv/bin/python</string>
        <string>$SCRIPT_DIR/timelapse_app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>StandardErrorPath</key>
    <string>/tmp/timelapse-menubar.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/timelapse-menubar.out</string>
</dict>
</plist>
EOF
echo "  Auto-start configured"

# Load and start the app
launchctl load "$LAUNCHAGENT_DIR/$PLIST_NAME"
sleep 1

echo ""
echo "=================================="
echo "  Installation Complete!"
echo "=================================="
echo ""
echo "Look for 'TL' in your menu bar (top right of screen)."
echo ""
echo "The app will start automatically when you log in."
echo ""
echo "To uninstall, run: ./uninstall.sh"
echo ""
