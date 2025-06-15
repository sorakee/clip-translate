import tkinter as tk
import threading
import os
import json
from settings import load_config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ConfigWatcher(FileSystemEventHandler):
    def __init__(self, overlay):
        self.overlay = overlay

    def on_modified(self, event):
        if event.src_path.endswith("config.json"):
            self.overlay.reload_config()


class OverlayWindow:
    def __init__(self):
        self.config = load_config()
        self.text = "Welcome! Waiting for translation..."
        self.root = None
        self.label = None
        self.config_path = "config.json"
        self.font_size = 14
        self.opacity = 0.8
        self.is_overlay_mode = True

    def start(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
    
    def reload_config(self):
        try:
            with open(self.config_path, "r") as f:
                new_config = json.load(f)
            self.config = new_config
            self.font_size = self.config.get("font_size", 14)
            self.opacity = self.config.get("opacity", 0.8)

            self.root.attributes('-alpha', self.opacity)
            self.text_widget.config(font=("Arial", self.font_size))
            print("🔄 Config reloaded.")
        except Exception as e:
            print("⚠️ Config reload failed:", e)

    def _run(self):
        TRANSPARENT_COLOR = "#123456"

        self.root = tk.Tk()
        self.root.wm_attributes('-transparentcolor', TRANSPARENT_COLOR)
        self.root.configure(bg=TRANSPARENT_COLOR)
        self.root.title("VN Translation Overlay")
        self.root.geometry("500x150")
        # self.root.configure(bg='black')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.config.get("opacity", 0.8))
        self.root.overrideredirect(True)
        self.root.bind("<F1>", lambda e: self.toggle_window_mode())
        observer = Observer()
        observer.schedule(ConfigWatcher(self), path=".", recursive=False)
        observer.start()
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Toggle Window Mode", command=self.toggle_window_mode)

        def show_menu(event):
            menu.tk_popup(event.x_root, event.y_root)

        self.root.bind("<Button-3>", show_menu)

        # Movable
        def start_move(e): self._x, self._y = e.x, e.y
        def do_move(e):
            dx, dy = e.x - self._x, e.y - self._y
            x, y = self.root.winfo_x() + dx, self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")

        self.root.bind("<Button-1>", start_move)
        self.root.bind("<B1-Motion>", do_move)

        # Label
        # Scrollable text widget
        text_frame = tk.Frame(self.root, bg='black')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.text_widget = tk.Text(
            text_frame,
            wrap="word",
            font=("Arial", self.font_size),
            fg="white",
            bg="black",
            relief="flat",
            state="disabled"
        )
        self.text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_widget.config(yscrollcommand=scrollbar.set)

        # Resize handle
        handle = tk.Label(self.root, bg='gray', width=2, cursor="bottom_right_corner")
        handle.place(relx=1.0, rely=1.0, anchor='se')

        def start_resize(event):
            self._resize_start_x = event.x_root
            self._resize_start_y = event.y_root
            self._start_width = self.root.winfo_width()
            self._start_height = self.root.winfo_height()

        def do_resize(event):
            dx = event.x_root - self._resize_start_x
            dy = event.y_root - self._resize_start_y
            new_width = max(self._start_width + dx, 200)
            new_height = max(self._start_height + dy, 100)
            self.root.geometry(f"{new_width}x{new_height}")

        handle.bind("<Button-1>", start_resize)
        handle.bind("<B1-Motion>", do_resize)

        self.root.mainloop()
    
    def toggle_window_mode(self):
        self.is_overlay_mode = not self.is_overlay_mode
        self.root.overrideredirect(self.is_overlay_mode)
        # Re-apply geometry so it doesn't jump
        self.root.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y()}")

    def update_text(self, new_text):
        self.text = new_text
        if self.text_widget:
            def apply_update():
                self.text_widget.config(state="normal")
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, new_text)
                self.text_widget.config(state="disabled")
                self.text_widget.yview_moveto(0)  # scroll to top
            self.text_widget.after(0, apply_update)

