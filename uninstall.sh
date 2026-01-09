#!/bin/bash
#
# Timelapse Menu Bar - Uninstaller
# This script stops the app and removes the auto-start configuration.
#

echo "=================================="
echo "  Timelapse Menu Bar - Uninstaller"
echo "=================================="
echo ""

PLIST_NAME="com.timelapse-menubar.plist"
LAUNCHAGENT_DIR="$HOME/Library/LaunchAgents"

# Stop and unload the launch agent
echo "Stopping app..."
if launchctl list | grep -q "$PLIST_NAME" 2>/dev/null; then
    launchctl unload "$LAUNCHAGENT_DIR/$PLIST_NAME" 2>/dev/null || true
    echo "  App stopped"
else
    echo "  App was not running"
fi

# Remove the plist file
echo ""
echo "Removing auto-start configuration..."
if [ -f "$LAUNCHAGENT_DIR/$PLIST_NAME" ]; then
    rm "$LAUNCHAGENT_DIR/$PLIST_NAME"
    echo "  Auto-start removed"
else
    echo "  No auto-start configuration found"
fi

echo ""
echo "=================================="
echo "  Uninstall Complete!"
echo "=================================="
echo ""
echo "The app has been stopped and will no longer start automatically."
echo ""
echo "The app files are still in this folder if you want to reinstall later."
echo "To completely remove, delete this folder."
echo ""
