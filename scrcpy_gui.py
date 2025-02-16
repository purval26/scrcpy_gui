import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

# Tooltip for explaining options
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
        label = tk.Label(tw, text=self.text, justify='left', background="#ffffe0",
                         relief='solid', borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

# Description for complicated options
option_descriptions = {
    "audio_source": "Select audio source: output (speaker), mic (microphone), or auto (default).",
    "video_encoder": "Select video encoding format, e.g., h264, hevc, av1.",
    "bit_rate": "Set video bit rate (higher = better quality, but more lag).",
    "max_size": "Limit resolution for smoother streaming (e.g., 1280).",
    "display_buffer": "Adjust buffer for low-latency (default: 50ms).",
    "turn_screen_off": "Turn device screen off while mirroring (saves power).",
    "record": "Record screen output to a file (e.g., video.mp4).",
    "tcpip": "Connect wirelessly (requires ADB over TCP/IP).",
    "otg": "Enable OTG mode for direct device connection.",
}

class ScrcpyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GreenScrcpy Controller")
        self.root.geometry("700x600")

        self.device_list = []
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)

        tabs = [
            ("Video", self.add_video_controls),
            ("Audio", self.add_audio_controls),
            ("Performance", self.add_perf_controls),
            ("Interaction", self.add_interaction_controls),
            ("Recording", self.add_recording_controls),
            ("Networking", self.add_networking_controls),
        ]

        for text, method in tabs:
            frame = ttk.Frame(notebook)
            method(frame)
            notebook.add(frame, text=text)

        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        start_btn = ttk.Button(self.root, text="START SCRCPY", command=self.start_scrcpy)
        start_btn.pack(pady=20, ipadx=20, ipady=8)

    def create_section(self, parent, controls):
        frame = ttk.Frame(parent)
        for i, (label_text, var_name, default) in enumerate(controls):
            lbl = ttk.Label(frame, text=label_text)
            lbl.grid(row=i, column=0, sticky='w', padx=5, pady=3)
            var = tk.StringVar(value=default)
            widget = ttk.Entry(frame, textvariable=var)
            widget.grid(row=i, column=1, sticky='ew', padx=5, pady=3)
            setattr(self, var_name, var)

            if var_name in option_descriptions:
                tooltip_label = tk.Label(frame, text="?", fg="yellow", font=('Helvetica', 10, 'bold'))
                tooltip_label.grid(row=i, column=2, sticky='w', padx=5, pady=3)
                ToolTip(tooltip_label, option_descriptions[var_name])

        frame.pack(fill='x', padx=5, pady=5)

    def add_video_controls(self, parent):
        controls = [
            ("Max Resolution:", "max_size", "1280"),
            ("Bit Rate (Mbps):", "bit_rate", "8M"),
            ("Video Encoder:", "video_encoder", "h264"),
        ]
        self.create_section(parent, controls)

    def add_audio_controls(self, parent):
        controls = [
            ("Audio Source:", "audio_source", "auto"),
        ]
        self.create_section(parent, controls)

    def add_perf_controls(self, parent):
        controls = [
            ("Display Buffer (ms):", "display_buffer", "50"),
        ]
        self.create_section(parent, controls)

    def add_interaction_controls(self, parent):
        controls = [
            ("Turn Screen Off:", "turn_screen_off", "false"),
        ]
        self.create_section(parent, controls)

    def add_recording_controls(self, parent):
        controls = [
            ("Record File:", "record", ""),
        ]
        self.create_section(parent, controls)

    def add_networking_controls(self, parent):
        controls = [
            ("Use Wireless TCP/IP:", "tcpip", "false"),
            ("OTG Mode:", "otg", "false"),
        ]
        self.create_section(parent, controls)

    def start_scrcpy(self):
        cmd = ['scrcpy']

        if self.max_size.get():
            cmd.extend(['--max-size', self.max_size.get()])
        if self.bit_rate.get():
            cmd.extend(['--bit-rate', self.bit_rate.get()])
        if self.video_encoder.get():
            cmd.extend(['--video-encoder', self.video_encoder.get()])
        if self.audio_source.get():
            cmd.extend(['--audio-source', self.audio_source.get()])
        if self.display_buffer.get():
            cmd.extend(['--display-buffer', self.display_buffer.get()])
        if self.turn_screen_off.get() == "true":
            cmd.append('--turn-screen-off')
        if self.record.get():
            cmd.extend(['--record', self.record.get()])
        if self.tcpip.get() == "true":
            cmd.append('--tcpip')
        if self.otg.get() == "true":
            cmd.append('--otg')

        try:
            subprocess.Popen(cmd)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrcpyGUI(root)
    root.mainloop()
