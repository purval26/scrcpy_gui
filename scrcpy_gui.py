import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import ttkbootstrap as tb  # Modern UI library

class ScrcpyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GreenScrcpy Controller")
        self.root.geometry("900x700")
        self.style = tb.Style("darkly")  # Modern UI Theme

        self.device_list = []
        self.create_widgets()
        
    def create_widgets(self):
        notebook = ttk.Notebook(self.root)

        # Creating different tabs
        tabs = [
            ("Video", self.add_video_controls),
            ("Audio", self.add_audio_controls),
            ("Device", self.add_device_controls),
            ("Window", self.add_window_controls),
            ("Input", self.add_input_controls),
            ("Mirroring", self.add_mirroring_controls),
            ("Performance", self.add_performance_controls),
            ("Advanced", self.add_advanced_controls),
            ("Other", self.add_other_controls)
        ]

        for text, method in tabs:
            frame = tb.Frame(notebook)
            method(frame)
            notebook.add(frame, text=text)

        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Start button
        start_btn = tb.Button(self.root, text="START MIRRORING", bootstyle="success",
                              command=self.start_scrcpy, padding=(10, 5))
        start_btn.pack(pady=20, ipadx=20, ipady=8)

    def create_section(self, parent, controls):
        """Creates labeled input fields and checkboxes dynamically."""
        frame = tb.Frame(parent)
        for i, (label, var_name, default, desc) in enumerate(controls):
            tb.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=3)

            if isinstance(default, bool):
                var = tk.BooleanVar(value=default)
                widget = tb.Checkbutton(frame, variable=var, bootstyle="success-round-toolbutton")
            else:
                var = tk.StringVar(value=default)
                widget = tb.Entry(frame, textvariable=var, bootstyle="info")

            setattr(self, var_name, var)
            widget.grid(row=i, column=1, sticky='ew', padx=5, pady=3)

            # Tooltip for complex options
            if desc:
                tb.Label(frame, text="?", bootstyle="warning-inverse",
                         padding=5).grid(row=i, column=2, padx=5)
            
        frame.pack(fill='x', padx=5, pady=5)

    def add_video_controls(self, parent):
        controls = [
            ("Bitrate (Mbps):", "bit_rate", "4", "Adjust video quality."),
            ("Max Size (px):", "max_size", "0", "Resize video output."),
            ("Crop (W:H:X:Y):", "crop", "", "Crop screen output."),
            ("Lock Orientation:", "lock_video_orientation", "0", "Force landscape/portrait."),
            ("No Video:", "no_video", False, "Disable video stream."),
            ("Encoder:", "encoder", "", "Choose video encoder manually."),
        ]
        self.create_section(parent, controls)

    def add_audio_controls(self, parent):
        controls = [
            ("No Audio:", "no_audio", False, "Disable audio."),
            ("Audio Source:", "audio_source", "auto", "Choose audio source."),
            ("Audio Bitrate (Kbps):", "audio_bitrate", "128", "Adjust sound quality."),
            ("Audio Buffer:", "audio_buffer", "50", "Reduce audio delay."),
        ]
        self.create_section(parent, controls)

    def add_device_controls(self, parent):
        controls = [
            ("Select Device:", "serial", "", "Choose a connected device."),
            ("Use Camera as Webcam:", "use_camera", False, "Turns phone camera into a webcam."),
            ("TCP/IP Mode:", "tcpip", False, "Wireless connection mode."),
            ("TCP/IP Port:", "port", "5555", "Port for wireless ADB."),
        ]
        self.create_section(parent, controls)

    def add_window_controls(self, parent):
        controls = [
            ("Fullscreen:", "fullscreen", False, "Open in fullscreen."),
            ("Always on Top:", "always_on_top", False, "Keep window on top."),
            ("Borderless:", "borderless", False, "Hide window borders."),
        ]
        self.create_section(parent, controls)

    def add_input_controls(self, parent):
        controls = [
            ("No Control:", "no_control", False, "Disable mouse/keyboard input."),
            ("Show Touches:", "show_touches", False, "Display touch feedback."),
            ("Disable Screensaver:", "disable_screensaver", False, "Prevent screen lock."),
        ]
        self.create_section(parent, controls)

    def add_mirroring_controls(self, parent):
        controls = [
            ("Rotation (0-3):", "rotation", "0", "Rotate screen output."),
            ("No Keyboard:", "no_keyboard", False, "Disable physical keyboard input."),
            ("No Mouse:", "no_mouse", False, "Disable mouse input."),
        ]
        self.create_section(parent, controls)

    def add_performance_controls(self, parent):
        controls = [
            ("Max FPS:", "max_fps", "60", "Limit frame rate."),
            ("No Display:", "no_display", False, "Run in background mode."),
            ("Render Driver:", "render_driver", "", "Change rendering method."),
        ]
        self.create_section(parent, controls)

    def add_advanced_controls(self, parent):
        controls = [
            ("Turn Screen Off:", "turn_screen_off", False, "Turn off phone screen."),
            ("Stay Awake:", "stay_awake", False, "Prevent phone sleep."),
            ("Force ADB Start:", "force_adb_start", False, "Ensure ADB is running."),
        ]
        self.create_section(parent, controls)

    def add_other_controls(self, parent):
        controls = [
            ("Record Screen:", "record_file", "", "Save screen recording."),
            ("Clipboard Synchronization:", "clipboard", False, "Sync PC & phone clipboard."),
            ("Disable VSync:", "disable_vsync", False, "Might improve performance."),
        ]
        self.create_section(parent, controls)

    def start_scrcpy(self):
        cmd = ['scrcpy']

        # Adding options dynamically
        if self.no_video.get(): cmd.append('--no-video')
        if self.bit_rate.get(): cmd.extend(['--bit-rate', f"{self.bit_rate.get()}M"])
        if self.max_size.get(): cmd.extend(['--max-size', self.max_size.get()])
        if self.crop.get(): cmd.extend(['--crop', self.crop.get()])
        if self.no_audio.get(): cmd.append('--no-audio')
        if self.audio_source.get(): cmd.extend(['--audio-source', self.audio_source.get()])
        if self.serial.get(): cmd.extend(['--serial', self.serial.get()])
        if self.use_camera.get(): cmd.append('--camera')
        if self.fullscreen.get(): cmd.append('--fullscreen')
        if self.always_on_top.get(): cmd.append('--always-on-top')
        if self.borderless.get(): cmd.append('--borderless')
        if self.rotation.get(): cmd.extend(['--rotation', self.rotation.get()])
        if self.max_fps.get(): cmd.extend(['--max-fps', self.max_fps.get()])
        if self.record_file.get(): cmd.extend(['--record', self.record_file.get()])

        try:
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy: {e}")

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = ScrcpyGUI(root)
    root.mainloop()
