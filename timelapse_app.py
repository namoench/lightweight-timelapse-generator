#!/usr/bin/env python3
"""Timelapse Menu Bar App - Create timelapses from photos using ffmpeg."""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

import rumps


class TimelapseApp(rumps.App):
    def __init__(self):
        super().__init__("TL", quit_button=None)

        self.selected_photos = []

        # Settings with defaults
        self.framerate = "24"
        self.resolution = "1920:-2"  # 1080p
        self.codec = "libx264"
        self.custom_command = None  # None means use generated command

        # Resolution map
        self.resolution_map = {
            "Original": None,
            "4K (3840)": "3840:-2",
            "1080p": "1920:-2",
            "720p": "1280:-2",
        }

        # Codec map
        self.codec_map = {
            "H.264": "libx264",
            "H.265/HEVC": "libx265",
            "ProRes": "prores_ks",
        }

        self.build_menu()

    def build_menu(self):
        """Build the menu structure."""
        self.menu.clear()

        # Photo selection
        photos_label = f"{len(self.selected_photos)} photos selected" if self.selected_photos else "No photos selected"
        self.menu.add(rumps.MenuItem(photos_label, callback=None))
        self.menu.add(rumps.MenuItem("Select Photos...", callback=self.select_photos))
        self.menu.add(rumps.MenuItem("Clear Selection", callback=self.clear_selection))
        self.menu.add(None)  # Separator

        # Framerate submenu
        framerate_menu = rumps.MenuItem("Framerate")
        for fps in ["12", "24", "30", "60"]:
            item = rumps.MenuItem(
                f"{'* ' if self.framerate == fps else '  '}{fps} fps",
                callback=lambda sender, f=fps: self.set_framerate(f)
            )
            framerate_menu.add(item)
        self.menu.add(framerate_menu)

        # Resolution submenu
        resolution_menu = rumps.MenuItem("Resolution")
        for name, value in self.resolution_map.items():
            is_selected = self.resolution == value
            item = rumps.MenuItem(
                f"{'* ' if is_selected else '  '}{name}",
                callback=lambda sender, v=value: self.set_resolution(v)
            )
            resolution_menu.add(item)
        self.menu.add(resolution_menu)

        # Codec submenu
        codec_menu = rumps.MenuItem("Codec")
        for name, value in self.codec_map.items():
            is_selected = self.codec == value
            item = rumps.MenuItem(
                f"{'* ' if is_selected else '  '}{name}",
                callback=lambda sender, v=value: self.set_codec(v)
            )
            codec_menu.add(item)
        self.menu.add(codec_menu)

        self.menu.add(None)  # Separator

        # Advanced
        cmd_label = "Edit Command... (custom)" if self.custom_command else "Edit Command..."
        self.menu.add(rumps.MenuItem(cmd_label, callback=self.edit_command))
        self.menu.add(rumps.MenuItem("Reset to Default", callback=self.reset_command))

        self.menu.add(None)  # Separator

        # Create button
        self.menu.add(rumps.MenuItem("Create Timelapse", callback=self.create_timelapse))

        self.menu.add(None)  # Separator
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))

    def get_ffmpeg_command(self, input_pattern, output_path):
        """Generate the ffmpeg command based on current settings."""
        if self.custom_command:
            # Replace placeholders in custom command
            cmd = self.custom_command.replace("{input}", input_pattern)
            cmd = cmd.replace("{output}", output_path)
            return cmd

        cmd_parts = [
            "ffmpeg", "-y",  # -y to overwrite without asking
            "-framerate", self.framerate,
            "-pattern_type", "glob",
            "-i", f"'{input_pattern}'",
        ]

        # Codec settings
        if self.codec == "libx264":
            cmd_parts.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p"])
        elif self.codec == "libx265":
            cmd_parts.extend(["-c:v", "libx265", "-pix_fmt", "yuv420p"])
        elif self.codec == "prores_ks":
            cmd_parts.extend(["-c:v", "prores_ks", "-profile:v", "3"])

        # Resolution
        if self.resolution:
            cmd_parts.extend(["-vf", f"scale={self.resolution}"])

        cmd_parts.append(f"'{output_path}'")

        return " ".join(cmd_parts)

    def select_photos(self, sender=None):
        """Open file picker to select photos using native macOS dialog."""
        script = '''
        tell application "Finder"
            activate
        end tell
        set theFiles to choose file with prompt "Select Photos for Timelapse" of type {"public.jpeg", "public.png", "public.tiff"} with multiple selections allowed
        set filePaths to ""
        repeat with aFile in theFiles
            set filePaths to filePaths & POSIX path of aFile & linefeed
        end repeat
        return filePaths
        '''

        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True
            )

            if result.returncode == 0 and result.stdout.strip():
                files = [f for f in result.stdout.strip().split("\n") if f]
                if files:
                    self.selected_photos = sorted(files)
                    self.build_menu()
                    rumps.notification(
                        "Timelapse",
                        "Photos Selected",
                        f"Selected {len(self.selected_photos)} photos"
                    )
        except Exception as e:
            rumps.alert("Error", f"Failed to open file picker: {e}")

    def clear_selection(self, sender=None):
        """Clear selected photos."""
        self.selected_photos = []
        self.build_menu()

    def set_framerate(self, fps):
        """Set the framerate."""
        self.framerate = fps
        self.custom_command = None  # Reset custom command when changing settings
        self.build_menu()

    def set_resolution(self, value):
        """Set the resolution."""
        self.resolution = value
        self.custom_command = None
        self.build_menu()

    def set_codec(self, value):
        """Set the codec."""
        self.codec = value
        self.custom_command = None
        self.build_menu()

    def edit_command(self, sender=None):
        """Show dialog to edit the ffmpeg command."""
        current_cmd = self.custom_command or self.get_ffmpeg_command("{input}", "{output}")

        response = rumps.Window(
            message="Edit the ffmpeg command.\nUse {input} for input pattern and {output} for output path.",
            title="Edit ffmpeg Command",
            default_text=current_cmd,
            ok="Save",
            cancel="Cancel",
            dimensions=(500, 100)
        ).run()

        if response.clicked:
            self.custom_command = response.text.strip()
            self.build_menu()

    def reset_command(self, sender=None):
        """Reset to default generated command."""
        self.custom_command = None
        self.framerate = "24"
        self.resolution = "1920:-2"
        self.codec = "libx264"
        self.build_menu()
        rumps.notification("Timelapse", "Reset", "Settings reset to defaults")

    def create_timelapse(self, sender=None):
        """Create the timelapse from selected photos."""
        if not self.selected_photos:
            rumps.alert("No Photos", "Please select photos first.")
            return

        # Create temp directory and copy/symlink photos with sequential names
        temp_dir = tempfile.mkdtemp(prefix="timelapse_")

        try:
            # Get extension from first file
            ext = Path(self.selected_photos[0]).suffix

            # Create symlinks with sequential names for proper ordering
            for i, photo in enumerate(self.selected_photos):
                link_name = os.path.join(temp_dir, f"img_{i:05d}{ext}")
                os.symlink(photo, link_name)

            # Output path with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_ext = ".mov" if self.codec == "prores_ks" else ".mp4"
            output_path = os.path.expanduser(f"~/Desktop/timelapse_{timestamp}{output_ext}")

            # Build input pattern
            input_pattern = os.path.join(temp_dir, f"*{ext}")

            # Get command
            cmd = self.get_ffmpeg_command(input_pattern, output_path)

            # Run ffmpeg
            rumps.notification("Timelapse", "Processing", f"Creating timelapse from {len(self.selected_photos)} photos...")

            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                rumps.notification(
                    "Timelapse Complete",
                    "Success!",
                    f"Saved to Desktop: timelapse_{timestamp}{output_ext}"
                )
            else:
                error_msg = result.stderr[-200:] if len(result.stderr) > 200 else result.stderr
                rumps.alert("ffmpeg Error", f"Failed to create timelapse:\n{error_msg}")

        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    TimelapseApp().run()
