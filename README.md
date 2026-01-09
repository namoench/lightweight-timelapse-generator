# Timelapse Menu Bar

I create a lot of timelapses of the night sky, it was getting tedious sorting all the photos from my SD card and then remembering the FFmpeg commands I need every time, so I built this tiny little FFMPEG timelapse generation app to live in the menu bar of my macbook. Feel free to do whatever you'd like with it, hope it helps! 

![Menu Bar](https://img.shields.io/badge/macOS-Menu%20Bar%20App-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- Lives in your menu bar - always one click away
- Select multiple photos from any folder (SD card, hard drive, etc.)
- Configurable settings:
  - **Framerate**: 12, 24, 30, or 60 fps
  - **Resolution**: Original, 4K, 1080p, or 720p
  - **Codec**: H.264, H.265/HEVC, or ProRes
- Edit the raw ffmpeg command for advanced users
- Exports to your Desktop with a timestamp
- Starts automatically when you log in

## Requirements

Before installing, you need:

1. **macOS** (tested on macOS Sonoma, should work on earlier versions)
2. **Python 3.8 or later**
3. **ffmpeg**

### Installing the Requirements

If you don't have Python 3 or ffmpeg, here's how to install them:

#### Option A: Using Homebrew (Recommended)

If you have [Homebrew](https://brew.sh/), open Terminal and run:

```bash
brew install python ffmpeg
```

#### Option B: Manual Installation

1. **Python**: Download from [python.org](https://www.python.org/downloads/)
2. **ffmpeg**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use Homebrew

## Installation

1. **Download this project**
   - Click the green "Code" button above, then "Download ZIP"
   - Unzip the downloaded file
   - Move the folder somewhere permanent (like your Documents folder)

2. **Open Terminal**
   - Press `Cmd + Space`, type "Terminal", press Enter

3. **Navigate to the folder**
   ```bash
   cd ~/Documents/timelapse-menubar
   ```
   (Adjust the path if you put it somewhere else)

4. **Run the installer**
   ```bash
   ./install.sh
   ```

5. **Done!** Look for "TL" in your menu bar.

## How to Use

1. Click **"TL"** in your menu bar (top right of your screen)
2. Click **"Select Photos..."** and choose your timelapse images
3. Adjust settings if needed (Framerate, Resolution, Codec)
4. Click **"Create Timelapse"**
5. Find your video on your Desktop!

### Tips

- Photos are sorted alphabetically, so name them sequentially (most cameras do this automatically)
- For best results, use photos that are all the same size
- H.264 is the most compatible codec; ProRes is best quality but larger files

## Uninstalling

Open Terminal, navigate to the app folder, and run:

```bash
./uninstall.sh
```

This stops the app and removes it from auto-start. Delete the folder to fully remove.

## Troubleshooting

**"TL" doesn't appear in menu bar**
- Make sure the installer completed without errors
- Try running `./install.sh` again

**"Select Photos" doesn't open a file picker**
- The first time you use it, macOS may ask for permission
- If it still doesn't work, check System Settings > Privacy & Security > Files and Folders

**ffmpeg errors**
- Make sure ffmpeg is installed: run `ffmpeg -version` in Terminal
- Try with fewer photos first to test

## License

MIT License - feel free to use, modify, and share!


