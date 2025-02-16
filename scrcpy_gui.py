import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class ScrcpyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GreenScrcpy Controller")
        self.root.geometry("800x600")
        self.set_custom_style()
        
        self.device_list = []  # Initialize device list
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
        self.style.map('TButton', 
                      background=[('active', '#27AE60'), ('disabled', '#444444')])

        # Checkbutton and Border styles
        self.style.configure('CheckBorder.TFrame', background=self.frame_color,
                           borderwidth=2, relief='solid', bordercolor=self.accent_color)
        self.style.configure('TCheckbutton', background=self.frame_color, 
                           foreground=self.fg_color, font=('Helvetica', 9))
        self.style.map('TCheckbutton', 
                     background=[('active', self.frame_color)],
                     indicatorcolor=[('selected', self.accent_color)])

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
        self.style.map('TNotebook.Tab', 
                      background=[('selected', self.frame_color)],
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
        start_btn = ttk.Button(self.root, 
                             text="START MIRRORING", 
                             style='TButton',
                             command=self.start_scrcpy)
        start_btn.pack(pady=20, ipadx=20, ipady=8)
        
    def create_section(self, parent, controls):
        frame = ttk.Frame(parent, style='TFrame')
        for i, (label, var_name, default) in enumerate(controls):
            if isinstance(default, bool):
                border_frame = ttk.Frame(frame, style='CheckBorder.TFrame')
                var = tk.BooleanVar(value=default)
                chk = ttk.Checkbutton(border_frame, text=label, variable=var, style='TCheckbutton')
                chk.pack(anchor='w', padx=5, pady=2)
                border_frame.grid(row=i, column=0, columnspan=2, sticky='ew', padx=5, pady=3)
                setattr(self, var_name, var)
            else:
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

    def refresh_devices(self):
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            devices = [line.split('\t')[0] for line in result.stdout.splitlines()[1:] if "device" in line]
            self.device_list = devices
            if hasattr(self, 'serial'):
                self.serial['values'] = devices
                if devices:
                    self.serial.set(devices[0])
        except Exception as e:
            messagebox.showerror("Error", f"ADB not found or error: {str(e)}")

    def start_scrcpy(self):
        cmd = ['scrcpy']
        
        if self.serial.get():
            cmd.extend(['--serial', self.serial.get()])
        
        try:
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy: {str(e)}")

    # Add required tab methods
    def add_video_controls(self, parent):
        controls = [
            ("Bitrate (Mbps):", "bit_rate", "4"),
            ("Max Size (px):", "max_size", "0"),
            ("Crop (W:H:X:Y):", "crop", ""),
            ("No Video:", "no_video", False)
        ]
        self.create_section(parent, controls)

    def add_audio_controls(self, parent):
        controls = [
            ("No Audio:", "no_audio", False),
            ("Audio Bitrate (Kbps):", "audio_bitrate", "128")
        ]
        self.create_section(parent, controls)

    def add_device_controls(self, parent):
        controls = [
            ("Select Device:", "serial", ""),
            ("TCP/IP Mode:", "tcpip", False)
        ]
        self.create_section(parent, controls)
        refresh_btn = ttk.Button(parent, text="Refresh Devices", command=self.refresh_devices, style='TButton')
        refresh_btn.pack(pady=5)

    def add_window_controls(self, parent):
        controls = [
            ("Fullscreen:", "fullscreen", False),
            ("Always on Top:", "always_on_top", False)
        ]
        self.create_section(parent, controls)

    def add_input_controls(self, parent):
        controls = [
            ("No Control:", "no_control", False),
            ("Touch Events:", "show_touches", False)
        ]
        self.create_section(parent, controls)

    def add_mirror_controls(self, parent):
        controls = [
            ("Rotation (0-3):", "rotation", "0")
        ]
        self.create_section(parent, controls)

    def add_perf_controls(self, parent):
        controls = [
            ("Max FPS:", "max_fps", "60")
        ]
        self.create_section(parent, controls)

    def add_advanced_controls(self, parent):
        controls = [
            ("Stay Awake:", "stay_awake", False)
        ]
        self.create_section(parent, controls)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrcpyGUI(root)
    root.mainloop()
