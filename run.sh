#!/bin/bash
# Launch the Timelapse menu bar app

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

source venv/bin/activate
python timelapse_app.py
