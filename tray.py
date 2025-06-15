from pystray import Icon, MenuItem as Item, Menu
from PIL import Image, ImageDraw
import threading
import tkinter as tk
from settings import load_config, save_config
import os

def create_image():
    img = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(img)
    draw.text((10, 25), "T", fill="white")
    return img

def open_settings():
    cfg = load_config()

    def apply_changes():
        cfg['opacity'] = float(opacity_var.get())
        cfg['font_size'] = int(font_var.get())
        cfg['auto_close_sec'] = int(auto_close_var.get())
        save_config(cfg)
        win.destroy()

    win = tk.Tk()
    win.title("Settings")
    win.geometry("300x200")

    tk.Label(win, text="Opacity (0.1–1.0):").pack()
    opacity_var = tk.StringVar(value=str(cfg['opacity']))
    tk.Entry(win, textvariable=opacity_var).pack()

    tk.Label(win, text="Font Size:").pack()
    font_var = tk.StringVar(value=str(cfg['font_size']))
    tk.Entry(win, textvariable=font_var).pack()

    tk.Label(win, text="Auto-Close (sec):").pack()
    auto_close_var = tk.StringVar(value=str(cfg['auto_close_sec']))
    tk.Entry(win, textvariable=auto_close_var).pack()

    tk.Button(win, text="Apply", command=apply_changes).pack(pady=10)
    win.mainloop()

def quit_app(icon, item):
    icon.stop()
    os._exit(0)

def run_tray():
    menu = Menu(Item("Settings", open_settings), Item("Quit", quit_app))
    icon = Icon("ClipTranslate", create_image(), menu=menu)
    icon.run()

def start_tray_thread():
    threading.Thread(target=run_tray, daemon=True).start()
