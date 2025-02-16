import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

# -----------------------------
# Tooltip class implementation
# -----------------------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
    
    def enter(self, event=None):
        self.schedule()
    
    def leave(self, event=None):
        self.unschedule()
        self.hidetip()
    
    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)
    
    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
    
    def showtip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            tw,
            text=self.text,
            justify='left',
            background="#ffffe0",
            relief='solid',
            borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)
    
    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

# -----------------------------
# Option descriptions dictionary
# -----------------------------
option_descriptions = {
    "crop": "Specifies the area of the device screen to mirror.\nFormat: W:H:X:Y (width:height:x_offset:y_offset).",
    "lock_video_orientation": "Locks the video orientation.\nAcceptable values: 0 (default), 1, 2, 3.",
    "record": "Records the mirroring session to the specified file path.",
    "record_format": "Specifies the container format for recording (e.g., mp4, mkv).",
    "tcpip": "Enables TCP/IP mode for device connection.\nRequires the device to be set to TCP/IP mode.",
    "port": "Specifies the TCP/IP port to use (default: 5555).",
    "display_id": "Specifies the display ID for devices with multiple displays.",
    "window_x": "X coordinate for the scrcpy window position.",
    "window_y": "Y coordinate for the scrcpy window position.",
    "window_width": "Width of the scrcpy window.",
    "window_height": "Height of the scrcpy window.",
    "prefer_texture_view": "Use TextureView instead of SurfaceView for mirroring.",
    "video_filter": "Apply a video filter (e.g., 'crop=800:600') to the video stream.",
    "render_driver": "Specify the render driver (e.g., 'opengl', 'd3d') to use.",
    "no_mipmaps": "Disable mipmaps during rendering.",
    "render_expired_frames": "Render expired frames to avoid frame drops.",
    "print_fps": "Display the current FPS in the console.",
    "turn_screen_off": "Turn the device screen off during mirroring.",
    "force_adb_forward": "Force ADB to forward the connection even if insecure.",
    "display_copy": "Copy the display properties instead of mirroring."
}

# -----------------------------
# Main Application Class
# -----------------------------
class ScrcpyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GreenScrcpy Controller")
        self.root.geometry("800x600")
        self.set_custom_style()
        
        self.device_list = []  # initialize device list
        self.create_widgets()

    def set_custom_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color scheme
        self.bg_color = "#2D2D2D"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#2ECC71"
        self.frame_color = "#3D3D3D"
        
        # Configure styles
        self.style.configure('.', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TFrame', background=self.frame_color)
        self.style.configure('TLabel', background=self.frame_color, foreground=self.fg_color)
        self.style.configure('TButton', background=self.accent_color, foreground="#000000",
                             font=('Helvetica', 10, 'bold'), padding=5)
        self.style.map('TButton', background=[('active', '#27AE60'), ('disabled', '#444444')])
        
        # Checkbutton and Border styles
        self.style.configure('CheckBorder.TFrame', background=self.frame_color,
                             borderwidth=2, relief='solid', bordercolor=self.accent_color)
        self.style.configure('TCheckbutton', background=self.frame_color,
                             foreground=self.fg_color, font=('Helvetica', 9))
        self.style.map('TCheckbutton', background=[('active', self.frame_color)])
        
        # Entry and Combobox styles
        self.style.configure('TEntry', fieldbackground="#444444",
                             foreground=self.fg_color, insertcolor=self.fg_color)
        self.style.configure('TCombobox', fieldbackground="#444444",
                             foreground=self.fg_color, selectbackground=self.accent_color)
        
        # Notebook styles
        self.style.configure('TNotebook', background=self.bg_color)
        self.style.configure('TNotebook.Tab',
                             background=self.bg_color,
                             foreground=self.fg_color,
                             padding=[10, 5],
                             font=('Helvetica', 9, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', self.frame_color)],
                       foreground=[('selected', self.accent_color)])
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.root, style='TNotebook')
        
        tabs = [
            ("Video", self.add_video_controls),
            ("Audio", self.add_audio_controls),
            ("Device", self.add_device_controls),
            ("Window", self.add_window_controls),
            ("Input", self.add_input_controls),
            ("Mirroring", self.add_mirror_controls),
            ("Performance", self.add_perf_controls),
            ("Advanced", self.add_advanced_controls)
        ]
        
        for text, method in tabs:
            frame = ttk.Frame(notebook, style='TFrame')
            method(frame)
            notebook.add(frame, text=text)
        
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Main start button
        start_btn = ttk.Button(self.root, text="START MIRRORING", style='TButton', command=self.start_scrcpy)
        start_btn.pack(pady=20, ipadx=20, ipady=8)
    
    def create_section(self, parent, controls):
        """
        Creates a section (a frame) of controls.
        For each option, if a tooltip description exists, a "?" icon is added.
        """
        frame = ttk.Frame(parent, style='TFrame')
        for i, (label_text, var_name, default) in enumerate(controls):
            if isinstance(default, bool):
                # Boolean option: display the checkbox in column 0.
                border_frame = ttk.Frame(frame, style='CheckBorder.TFrame')
                var = tk.BooleanVar(value=default)
                chk = ttk.Checkbutton(border_frame, text=label_text, variable=var, style='TCheckbutton')
                chk.pack(anchor='w', padx=5, pady=2)
                border_frame.grid(row=i, column=0, sticky='ew', padx=5, pady=3)
                setattr(self, var_name, var)
                # Add tooltip if description exists.
                if var_name in option_descriptions:
                    tooltip_label = tk.Label(frame, text="?", fg="yellow", bg=self.frame_color, font=('Helvetica', 10, 'bold'))
                    tooltip_label.grid(row=i, column=1, sticky='w', padx=5, pady=3)
                    ToolTip(tooltip_label, option_descriptions[var_name])
                else:
                    tk.Label(frame, text="").grid(row=i, column=1, padx=5, pady=3)
            else:
                # Non-boolean option: label in column 0, entry/combobox in column 1.
                lbl = ttk.Label(frame, text=label_text, style='TLabel')
                lbl.grid(row=i, column=0, sticky='w', padx=5, pady=3)
                var = tk.StringVar(value=default)
                if var_name == "serial":
                    widget = ttk.Combobox(frame, textvariable=var, values=self.device_list, style='TCombobox')
                    self.serial_widget = widget  # Save reference for device refresh.
                else:
                    widget = ttk.Entry(frame, textvariable=var, style='TEntry')
                setattr(self, var_name, var)
                widget.grid(row=i, column=1, sticky='ew', padx=5, pady=3)
                # Add tooltip if available.
                if var_name in option_descriptions:
                    tooltip_label = tk.Label(frame, text="?", fg="yellow", bg=self.frame_color, font=('Helvetica', 10, 'bold'))
                    tooltip_label.grid(row=i, column=2, sticky='w', padx=5, pady=3)
                    ToolTip(tooltip_label, option_descriptions[var_name])
        frame.pack(fill='x', padx=5, pady=5)
    
    def refresh_devices(self):
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            devices = [line.split('\t')[0] for line in result.stdout.splitlines()[1:] if "device" in line]
            self.device_list = devices
            if hasattr(self, 'serial_widget'):
                self.serial_widget['values'] = devices
                if devices:
                    self.serial.set(devices[0])
        except Exception as e:
            messagebox.showerror("Error", f"ADB not found or error: {str(e)}")
    
    def start_scrcpy(self):
        cmd = ['scrcpy']
        # --- Video Options ---
        if self.bit_rate.get() and self.bit_rate.get() != "4":
            cmd.extend(['--bit-rate', f'{self.bit_rate.get()}M'])
        if self.max_size.get() and self.max_size.get() != "0":
            cmd.extend(['--max-size', self.max_size.get()])
        if self.crop.get():
            cmd.extend(['--crop', self.crop.get()])
        if self.lock_video_orientation.get() and self.lock_video_orientation.get() != "0":
            cmd.extend(['--lock-video-orientation', self.lock_video_orientation.get()])
        if self.record.get():
            cmd.extend(['--record', self.record.get()])
        if self.record_format.get():
            cmd.extend(['--record-format', self.record_format.get()])
        if self.no_video.get():
            cmd.append('--no-video')
        
        # --- Audio Options ---
        if self.no_audio.get():
            cmd.append('--no-audio')
        if self.audio_bitrate.get() and self.audio_bitrate.get() != "128":
            cmd.extend(['--audio-bit-rate', self.audio_bitrate.get()])
        if self.audio_buffer.get() and self.audio_buffer.get() != "50":
            cmd.extend(['--audio-buffer', self.audio_buffer.get()])
        
        # --- Device Options ---
        if self.serial.get():
            cmd.extend(['--serial', self.serial.get()])
        if self.tcpip.get():
            cmd.extend(['--tcpip', self.port.get()])
        if self.display_id.get():
            cmd.extend(['--display-id', self.display_id.get()])
        
        # --- Window Options ---
        if self.window_title.get() and self.window_title.get() != "scrcpy":
            cmd.extend(['--window-title', self.window_title.get()])
        if self.window_x.get():
            cmd.extend(['--window-x', self.window_x.get()])
        if self.window_y.get():
            cmd.extend(['--window-y', self.window_y.get()])
        if self.window_width.get():
            cmd.extend(['--window-width', self.window_width.get()])
        if self.window_height.get():
            cmd.extend(['--window-height', self.window_height.get()])
        if self.fullscreen.get():
            cmd.append('--fullscreen')
        if self.always_on_top.get():
            cmd.append('--always-on-top')
        if self.borderless.get():
            cmd.append('--borderless')
        
        # --- Input Options ---
        if self.no_control.get():
            cmd.append('--no-control')
        if self.show_touches.get():
            cmd.append('--show-touches')
        if self.disable_screensaver.get():
            cmd.append('--disable-screensaver')
        
        # --- Mirroring Options ---
        if self.rotation.get() and self.rotation.get() != "0":
            cmd.extend(['--rotation', self.rotation.get()])
        if self.no_keyboard.get():
            cmd.append('--no-keyboard')
        if self.no_mouse.get():
            cmd.append('--no-mouse')
        if self.prefer_texture_view.get():
            cmd.append('--prefer-texture-view')
        if self.video_filter.get():
            cmd.extend(['--video-filter', self.video_filter.get()])
        
        # --- Performance Options ---
        if self.max_fps.get() and self.max_fps.get() != "60":
            cmd.extend(['--max-fps', self.max_fps.get()])
        if self.no_display.get():
            cmd.append('--no-display')
        if self.render_driver.get():
            cmd.extend(['--render-driver', self.render_driver.get()])
        if self.no_mipmaps.get():
            cmd.append('--no-mipmaps')
        if self.render_expired_frames.get():
            cmd.append('--render-expired-frames')
        if self.print_fps.get():
            cmd.append('--print-fps')
        
        # --- Advanced Options ---
        if self.turn_screen_off.get():
            cmd.append('--turn-screen-off')
        if self.stay_awake.get():
            cmd.append('--stay-awake')
        if self.force_adb_forward.get():
            cmd.append('--force-adb-forward')
        if self.display_copy.get():
            cmd.append('--display-copy')
        
        try:
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy: {str(e)}")
    
    def take_screenshot(self):
        try:
            subprocess.Popen(['scrcpy', '--screenshot'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to take screenshot: {str(e)}")
    
    # --- Video Tab ---
    def add_video_controls(self, parent):
        controls = [
            ("Bitrate (Mbps):", "bit_rate", "4"),
            ("Max Size (px):", "max_size", "0"),
            ("Crop (W:H:X:Y):", "crop", ""),
            ("Lock Video Orientation (0-3):", "lock_video_orientation", "0"),
            ("Record File:", "record", ""),
            ("Record Format:", "record_format", ""),
            ("No Video:", "no_video", False)
        ]
        self.create_section(parent, controls)
    
    # --- Audio Tab ---
    def add_audio_controls(self, parent):
        controls = [
            ("No Audio:", "no_audio", False),
            ("Audio Bitrate (Kbps):", "audio_bitrate", "128"),
            ("Audio Buffer:", "audio_buffer", "50")
        ]
        self.create_section(parent, controls)
    
    # --- Device Tab ---
    def add_device_controls(self, parent):
        controls = [
            ("Select Device:", "serial", ""),
            ("TCP/IP Mode:", "tcpip", False),
            ("TCP/IP Port:", "port", "5555"),
            ("Display ID:", "display_id", "")
        ]
        self.create_section(parent, controls)
        refresh_btn = ttk.Button(parent, text="Refresh Devices", command=self.refresh_devices, style='TButton')
        refresh_btn.pack(pady=5)
    
    # --- Window Tab ---
    def add_window_controls(self, parent):
        controls = [
            ("Window Title:", "window_title", "scrcpy"),
            ("Window X:", "window_x", ""),
            ("Window Y:", "window_y", ""),
            ("Window Width:", "window_width", ""),
            ("Window Height:", "window_height", ""),
            ("Fullscreen:", "fullscreen", False),
            ("Always on Top:", "always_on_top", False),
            ("Borderless:", "borderless", False)
        ]
        self.create_section(parent, controls)
    
    # --- Input Tab ---
    def add_input_controls(self, parent):
        controls = [
            ("No Control:", "no_control", False),
            ("Show Touches:", "show_touches", False),
            ("Disable Screensaver:", "disable_screensaver", False)
        ]
        self.create_section(parent, controls)
    
    # --- Mirroring Tab ---
    def add_mirror_controls(self, parent):
        controls = [
            ("Rotation (0-3):", "rotation", "0"),
            ("No Keyboard:", "no_keyboard", False),
            ("No Mouse:", "no_mouse", False),
            ("Prefer Texture View:", "prefer_texture_view", False),
            ("Video Filter:", "video_filter", "")
        ]
        self.create_section(parent, controls)
    
    # --- Performance Tab ---
    def add_perf_controls(self, parent):
        controls = [
            ("Max FPS:", "max_fps", "60"),
            ("No Display:", "no_display", False),
            ("Render Driver:", "render_driver", ""),
            ("No Mipmaps:", "no_mipmaps", False),
            ("Render Expired Frames:", "render_expired_frames", False),
            ("Print FPS:", "print_fps", False)
        ]
        self.create_section(parent, controls)
    
    # --- Advanced Tab ---
    def add_advanced_controls(self, parent):
        controls = [
            ("Turn Screen Off:", "turn_screen_off", False),
            ("Stay Awake:", "stay_awake", False),
            ("Force ADB Forward:", "force_adb_forward", False),
            ("Display Copy:", "display_copy", False)
        ]
        self.create_section(parent, controls)
        screenshot_btn = ttk.Button(parent, text="Take Screenshot", command=self.take_screenshot, style='TButton')
        screenshot_btn.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrcpyGUI(root)
    root.mainloop()
