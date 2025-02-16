import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class ScrcpyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GreenScrcpy Controller")
        self.root.geometry("800x600")
        self.set_custom_style()
        
        self.create_widgets()
        self.device_list = []
        
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
        self.style.configure('TNotebook.Tab', background=self.bg_color, 
                            foreground=self.fg_color, padding=[10, 5], font=('Helvetica', 9, 'bold'))
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
        
        # Custom start button
        start_btn = ttk.Button(self.root, text="START MIRRORING", style='TButton', command=self.start_scrcpy)
        start_btn.pack(pady=20, ipadx=20, ipady=8)
        
    def create_section(self, parent, controls):
        frame = ttk.Frame(parent, style='TFrame')
        for i, (label, var_name, default) in enumerate(controls):
            if isinstance(default, bool):
                # Checkbox with border and label
                border_frame = ttk.Frame(frame, style='CheckBorder.TFrame')
                var = tk.BooleanVar(value=default)
                chk = ttk.Checkbutton(border_frame, text=label, variable=var, style='TCheckbutton')
                chk.pack(anchor='w', padx=5, pady=2)
                border_frame.grid(row=i, column=0, columnspan=2, sticky='ew', padx=5, pady=3)
                setattr(self, var_name, var)
            else:
                # Regular input with label
                lbl = ttk.Label(frame, text=label, style='TLabel')
                lbl.grid(row=i, column=0, sticky='w', padx=5, pady=3)
                
                var = tk.StringVar(value=default)
                if var_name == "serial":
                    widget = ttk.Combobox(frame, textvariable=var, values=self.device_list, style='TCombobox')
                else:
                    widget = ttk.Entry(frame, textvariable=var, style='TEntry')
                
                setattr(self, var_name, var)
                widget.grid(row=i, column=1, sticky='ew', padx=5, pady=3)
        
        frame.pack(fill='x', padx=5, pady=5)

    # Video Controls
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

    # Audio Controls
    def add_audio_controls(self, parent):
        controls = [
            ("No Audio:", "no_audio", False),
            ("Audio Bitrate (Kbps):", "audio_bitrate", "128"),
            ("Audio Buffer:", "audio_buffer", "50")
        ]
        self.create_section(parent, controls)

    # Device Controls
    def add_device_controls(self, parent):
        controls = [
            ("Select Device:", "serial", ""),
            ("TCP/IP Mode:", "tcpip", False),
            ("TCP/IP Port:", "port", "5555")
        ]
        self.create_section(parent, controls)

    # Window Controls
    def add_window_controls(self, parent):
        controls = [
            ("Window Title:", "window_title", "scrcpy"),
            ("Fullscreen:", "fullscreen", False),
            ("Always on Top:", "always_on_top", False),
            ("Borderless:", "borderless", False)
        ]
        self.create_section(parent, controls)

    # Input Controls
    def add_input_controls(self, parent):
        controls = [
            ("No Control:", "no_control", False),
            ("Touch Events:", "show_touches", False),
            ("Disable Screensaver:", "disable_screensaver", False)
        ]
        self.create_section(parent, controls)

    # Mirroring Controls
    def add_mirror_controls(self, parent):
        controls = [
            ("Rotation (0-3):", "rotation", "0"),
            ("No Keyboard:", "no_keyboard", False),
            ("No Mouse:", "no_mouse", False)
        ]
        self.create_section(parent, controls)

    # Performance Controls
    def add_perf_controls(self, parent):
        controls = [
            ("Max FPS:", "max_fps", "60"),
            ("No Display:", "no_display", False),
            ("Render Driver:", "render_driver", "")
        ]
        self.create_section(parent, controls)

    # Advanced Controls
    def add_advanced_controls(self, parent):
        controls = [
            ("Turn Screen Off:", "turn_screen_off", False),
            ("Stay Awake:", "stay_awake", False),
            ("Force ADB Start:", "force_adb_start", False)
        ]
        self.create_section(parent, controls)

    def start_scrcpy(self):
        try:
            subprocess.Popen(['scrcpy'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrcpyGUI(root)
    root.mainloop()
