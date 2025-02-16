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

    # [Keep all other methods (refresh_devices, start_scrcpy) unchanged]

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrcpyGUI(root)
    root.mainloop()
