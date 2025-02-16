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

        # Creating different tabs with multiple options in each
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
        """
        Dynamically creates a section with labels, input fields or checkboxes,
        and a tooltip ("?") if a description is provided.
        """
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

            # Add a tooltip icon if a description exists
            if desc:
                tip = tb.Label(frame, text="?", bootstyle="warning-inverse", padding=5)
                tip.grid(row=i, column=2, sticky='w', padx=5, pady=3)
                ToolTip(tip, desc)
            
        frame.pack(fill='x', padx=5, pady=5)

    def add_video_controls(self, parent):
        controls = [
            ("Bitrate (Mbps):", "bit_rate", "4", "Adjust video quality (higher equals better quality, more bandwidth)."),
            ("Max Size (px):", "max_size", "0", "Limit the resolution for smoother performance."),
            ("Crop (W:H:X:Y):", "crop", "", "Crop the mirrored screen (format: width:height:x:y)."),
            ("Lock Orientation:", "lock_video_orientation", "0", "Force a specific orientation (0-3)."),
            ("No Video:", "no_video", False, "Disable video stream entirely."),
            ("Encoder:", "encoder", "", "Select a specific video encoder (e.g., h264, hevc)."),
        ]
        self.create_section(parent, controls)

    def add_audio_controls(self, parent):
        controls = [
            ("No Audio:", "no_audio", False, "Disable audio stream."),
            ("Audio Source:", "audio_source", "auto", "Select audio source: auto, output (speaker), or mic."),
            ("Audio Bitrate (Kbps):", "audio_bitrate", "128", "Set audio bitrate (higher equals better quality)."),
            ("Audio Buffer (ms):", "audio_buffer", "50", "Set buffer to reduce audio delay."),
        ]
        self.create_section(parent, controls)

    def add_device_controls(self, parent):
        controls = [
            ("Select Device:", "serial", "", "Choose a connected device (via ADB)."),
            ("Use Camera as Webcam:", "use_camera", False, "Use the device's camera as a webcam."),
            ("TCP/IP Mode:", "tcpip", False, "Enable wireless connection (ADB over TCP/IP)."),
            ("TCP/IP Port:", "port", "5555", "Specify port for wireless ADB."),
        ]
        self.create_section(parent, controls)

    def add_window_controls(self, parent):
        controls = [
            ("Fullscreen:", "fullscreen", False, "Launch scrcpy in fullscreen mode."),
            ("Always on Top:", "always_on_top", False, "Keep the scrcpy window always on top."),
            ("Borderless:", "borderless", False, "Run scrcpy without window borders."),
        ]
        self.create_section(parent, controls)

    def add_input_controls(self, parent):
        controls = [
            ("No Control:", "no_control", False, "Disable control of the device from your PC."),
            ("Show Touches:", "show_touches", False, "Display touch indicators on the device screen."),
            ("Disable Screensaver:", "disable_screensaver", False, "Prevent the device from sleeping."),
        ]
        self.create_section(parent, controls)

    def add_mirroring_controls(self, parent):
        controls = [
            ("Rotation (0-3):", "rotation", "0", "Rotate the mirrored screen (0, 1, 2, or 3)."),
            ("No Keyboard:", "no_keyboard", False, "Disable physical keyboard input."),
            ("No Mouse:", "no_mouse", False, "Disable mouse input."),
        ]
        self.create_section(parent, controls)

    def add_performance_controls(self, parent):
        controls = [
            ("Max FPS:", "max_fps", "60", "Limit the frame rate to reduce CPU usage."),
            ("No Display:", "no_display", False, "Run scrcpy in headless mode (no window)."),
            ("Render Driver:", "render_driver", "", "Force a specific render driver (e.g., opengl, d3d)."),
        ]
        self.create_section(parent, controls)

    def add_advanced_controls(self, parent):
        controls = [
            ("Turn Screen Off:", "turn_screen_off", False, "Turn off the device screen while mirroring."),
            ("Stay Awake:", "stay_awake", False, "Prevent the device from sleeping."),
            ("Force ADB Start:", "force_adb_start", False, "Force start the ADB server."),
        ]
        self.create_section(parent, controls)

    def add_other_controls(self, parent):
        controls = [
            ("Record Screen:", "record_file", "", "Save a recording of the mirroring session."),
            ("Clipboard Sync:", "clipboard", False, "Synchronize clipboard between PC and device."),
            ("Disable VSync:", "disable_vsync", False, "Disable VSync to potentially improve performance."),
        ]
        self.create_section(parent, controls)

    def start_scrcpy(self):
        cmd = ['scrcpy']

        # Video options
        if self.no_video.get(): cmd.append('--no-video')
        if self.bit_rate.get(): cmd.extend(['--bit-rate', f"{self.bit_rate.get()}M"])
        if self.max_size.get(): cmd.extend(['--max-size', self.max_size.get()])
        if self.crop.get(): cmd.extend(['--crop', self.crop.get()])
        # (Additional video options like lock_video_orientation and encoder could be added similarly)

        # Audio options
        if self.no_audio.get(): cmd.append('--no-audio')
        if self.audio_source.get(): cmd.extend(['--audio-source', self.audio_source.get()])
        # (Other audio options could be appended here)

        # Device options
        if self.serial.get(): cmd.extend(['--serial', self.serial.get()])
        if self.use_camera.get(): cmd.append('--camera')
        if self.tcpip.get(): cmd.append('--tcpip')
        if self.port.get(): cmd.extend(['--port', self.port.get()])

        # Window options
        if self.fullscreen.get(): cmd.append('--fullscreen')
        if self.always_on_top.get(): cmd.append('--always-on-top')
        if self.borderless.get(): cmd.append('--borderless')

        # Input options
        if self.no_control.get(): cmd.append('--no-control')
        if self.show_touches.get(): cmd.append('--show-touches')
        if self.disable_screensaver.get(): cmd.append('--disable-screensaver')

        # Mirroring options
        if self.rotation.get(): cmd.extend(['--rotation', self.rotation.get()])
        if self.no_keyboard.get(): cmd.append('--no-keyboard')
        if self.no_mouse.get(): cmd.append('--no-mouse')

        # Performance options
        if self.max_fps.get(): cmd.extend(['--max-fps', self.max_fps.get()])
        if self.no_display.get(): cmd.append('--no-display')
        if self.render_driver.get(): cmd.extend(['--render-driver', self.render_driver.get()])

        # Advanced options
        if self.turn_screen_off.get(): cmd.append('--turn-screen-off')
        if self.stay_awake.get(): cmd.append('--stay-awake')
        if self.force_adb_start.get(): cmd.append('--force-adb-start')

        # Other options
        if self.record_file.get(): cmd.extend(['--record', self.record_file.get()])
        if self.clipboard.get(): cmd.append('--clipboard')
        if self.disable_vsync.get(): cmd.append('--disable-vsync')

        try:
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy: {e}")

# Tooltip class for showing explanations
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
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
        if hasattr(self, "id") and self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def showtip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left', background="#ffffe0",
                         relief='solid', borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = ScrcpyGUI(root)
    root.mainloop()
