import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class ScrcpyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("scrcpy GUI Controller")
        self.root.geometry("800x600")
        
        self.device_list = []
        self.create_widgets()
        
    def create_widgets(self):
        # Notebook for different categories
        notebook = ttk.Notebook(self.root)
        
        # Video Tab
        video_frame = ttk.Frame(notebook)
        self.add_video_controls(video_frame)
        notebook.add(video_frame, text="Video")
        
        # Audio Tab
        audio_frame = ttk.Frame(notebook)
        self.add_audio_controls(audio_frame)
        notebook.add(audio_frame, text="Audio")
        
        # Device Tab
        device_frame = ttk.Frame(notebook)
        self.add_device_controls(device_frame)
        notebook.add(device_frame, text="Device")
        
        # Window Tab
        window_frame = ttk.Frame(notebook)
        self.add_window_controls(window_frame)
        notebook.add(window_frame, text="Window")
        
        # Input Tab
        input_frame = ttk.Frame(notebook)
        self.add_input_controls(input_frame)
        notebook.add(input_frame, text="Input")
        
        # Mirroring Tab
        mirror_frame = ttk.Frame(notebook)
        self.add_mirror_controls(mirror_frame)
        notebook.add(mirror_frame, text="Mirroring")
        
        # Performance Tab
        perf_frame = ttk.Frame(notebook)
        self.add_perf_controls(perf_frame)
        notebook.add(perf_frame, text="Performance")
        
        # Advanced Tab
        advanced_frame = ttk.Frame(notebook)
        self.add_advanced_controls(advanced_frame)
        notebook.add(advanced_frame, text="Advanced")
        
        notebook.pack(expand=True, fill='both')
        
        # Start button
        start_btn = ttk.Button(self.root, text="Start scrcpy", command=self.start_scrcpy)
        start_btn.pack(pady=10)
        
    def add_video_controls(self, parent):
        controls = [
            ("Bitrate (Mbps):", "bit_rate", "4"),
            ("Max Size (px):", "max_size", "0"),
            ("Crop (W:H:X:Y):", "crop", ""),
            ("Lock Video Orientation:", "lock_video_orientation", "0"),
            ("Encoder:", "encoder", ""),
            ("No Video:", "no_video", False)
        ]
        self.create_section(parent, controls)

    def add_audio_controls(self, parent):
        controls = [
            ("No Audio:", "no_audio", False),
            ("Audio Bitrate (Kbps):", "audio_bitrate", "128"),
            ("Audio Buffer:", "audio_buffer", "50")
        ]
        self.create_section(parent, controls)

    def add_device_controls(self, parent):
        # Here, using an empty string as the default for serial.
        controls = [
            ("Select Device:", "serial", ""),
            ("TCP/IP Mode:", "tcpip", False),
            ("TCP/IP Port:", "port", "5555")
        ]
        self.create_section(parent, controls)
        refresh_btn = ttk.Button(parent, text="Refresh Devices", command=self.refresh_devices)
        refresh_btn.pack(pady=5)
        # Populate devices initially
        self.refresh_devices()

    def add_window_controls(self, parent):
        controls = [
            ("Window Title:", "window_title", "scrcpy"),
            ("Fullscreen:", "fullscreen", False),
            ("Always on Top:", "always_on_top", False),
            ("Borderless:", "borderless", False)  # Fixed syntax error here.
        ]
        self.create_section(parent, controls)

    def add_input_controls(self, parent):
        controls = [
            ("No Control:", "no_control", False),
            ("Touch Events:", "show_touches", False),
            ("Disable Screensaver:", "disable_screensaver", False)
        ]
        self.create_section(parent, controls)

    def add_mirror_controls(self, parent):
        controls = [
            ("Rotation (0-3):", "rotation", "0"),
            ("No Keyboard:", "no_keyboard", False),
            ("No Mouse:", "no_mouse", False)
        ]
        self.create_section(parent, controls)

    def add_perf_controls(self, parent):
        controls = [
            ("Max FPS:", "max_fps", "60"),
            ("No Display:", "no_display", False),
            ("Render Driver:", "render_driver", "")
        ]
        self.create_section(parent, controls)

    def add_advanced_controls(self, parent):
        controls = [
            ("Turn Screen Off:", "turn_screen_off", False),
            ("Stay Awake:", "stay_awake", False),
            ("Force ADB Start:", "force_adb_start", False)
        ]
        self.create_section(parent, controls)

    def create_section(self, parent, controls):
        frame = ttk.Frame(parent)
        for i, (label, var_name, default) in enumerate(controls):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5)
            if isinstance(default, bool):
                var = tk.BooleanVar(value=default)
                widget = ttk.Checkbutton(frame, variable=var)
            else:
                var = tk.StringVar(value=default)
                if var_name == "serial":
                    widget = ttk.Combobox(frame, textvariable=var, values=self.device_list)
                    # Save the combobox widget for later updates
                    self.serial_widget = widget
                else:
                    widget = ttk.Entry(frame, textvariable=var)
            setattr(self, var_name, var)
            widget.grid(row=i, column=1, sticky='ew', padx=5)
        frame.pack(fill='x', padx=5, pady=5)

    def refresh_devices(self):
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            # Skip the first line (header) and ignore empty lines.
            devices = [line.split('\t')[0] for line in result.stdout.splitlines()[1:] if line.strip()]
            self.device_list = devices
            # If the serial control's combobox widget exists, update its values.
            if hasattr(self, 'serial_widget'):
                self.serial_widget['values'] = devices
                if devices:
                    self.serial.set(devices[0])
        except Exception as e:
            messagebox.showerror("Error", f"ADB not found or error: {str(e)}")

    def start_scrcpy(self):
        cmd = ['scrcpy']
        
        # Video options
        if self.no_video.get():
            cmd.append('--no-video')
        if (bitrate := self.bit_rate.get()) and bitrate != "4":
            cmd.extend(['--bit-rate', f'{bitrate}M'])
        if (max_size := self.max_size.get()) and max_size != "0":
            cmd.extend(['--max-size', max_size])
        if (crop := self.crop.get()):
            cmd.extend(['--crop', crop])
        
        # Audio options
        if self.no_audio.get():
            cmd.append('--no-audio')
        if (audio_br := self.audio_bitrate.get()) and audio_br != "128":
            cmd.extend(['--audio-bit-rate', audio_br])
        
        # Device options
        if (serial := self.serial.get()):
            cmd.extend(['--serial', serial])
        if self.tcpip.get():
            cmd.extend(['--tcpip', self.port.get()])
        
        # Window options
        if (title := self.window_title.get()) != "scrcpy":
            cmd.extend(['--window-title', title])
        if self.fullscreen.get():
            cmd.append('--fullscreen')
        if self.always_on_top.get():
            cmd.append('--always-on-top')
        if self.borderless.get():
            cmd.append('--borderless')
        
        # Advanced options
        if self.turn_screen_off.get():
            cmd.append('--turn-screen-off')
        if self.stay_awake.get():
            cmd.append('--stay-awake')
        
        try:
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrcpyGUI(root)
    root.mainloop()
