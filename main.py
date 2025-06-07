import cv2
import numpy as np
import pyautogui
import pydirectinput as pdi
import time
import tkinter as tk
import threading
import pytesseract
import queue
import maps
import config
from dhooks import Webhook

hook = Webhook(config.DC_webhook)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pdi.FAILSAFE = False

#threading
pause_event = threading.Event()
pause_event.set()
status_queue = queue.Queue()
paused_state = 0
status_lock = threading.Lock()

polo = cv2.imread('pic\\polo.PNG', cv2.IMREAD_UNCHANGED)
if polo is None:
    raise FileNotFoundError("rune.PNG not found")
if polo.shape[2] == 4:  # Has alpha channel
    polo = cv2.cvtColor(polo, cv2.COLOR_BGRA2BGR)

violet = cv2.imread('pic\\violet.PNG', cv2.IMREAD_UNCHANGED)
if violet is None:
    raise FileNotFoundError("violet.PNG not found")
if violet.shape[2] == 4:  # Has alpha channel
    violet = cv2.cvtColor(violet, cv2.COLOR_BGRA2BGR)

died = cv2.imread('pic\\died.PNG', cv2.IMREAD_UNCHANGED)
if died is None:
    raise FileNotFoundError("died.PNG not found")
if died.shape[2] == 4:  # Has alpha channel
    died = cv2.cvtColor(died, cv2.COLOR_BGRA2BGR)

def lie():
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Define yellow range (tune as needed)
    color1 = np.array([14, 159, 192])
    color2 = np.array([0, 204, 255])
    mask1 = cv2.inRange(img, color1, color1)
    mask2 = cv2.inRange(img, color2, color2)

    # Create mask
    mask = cv2.bitwise_or(mask1, mask2)

    # OCR
    text = pytesseract.image_to_string(mask)
    #cv2.imwrite('lie.jpg', mask)

    if "Lie Detector" in text:
        set_paused(2)
        hook.send("<@&1380790894248202282> CAPTCHA")
        print("CAPTCHA\nCAPTCHA\nCAPTCHA\nCAPTCHA\nCAPTCHA")
    else:
        threshold = 0.8
        res3 = cv2.matchTemplate(img, polo, cv2.TM_CCOEFF_NORMED)
        min_val3, max_val3, min_loc3, max_loc3 = cv2.minMaxLoc(res3)

        res4 = cv2.matchTemplate(img, violet, cv2.TM_CCOEFF_NORMED)
        min_val4, max_val4, min_loc4, max_loc4 = cv2.minMaxLoc(res4)

        res5 = cv2.matchTemplate(img, died, cv2.TM_CCOEFF_NORMED)
        min_val5, max_val5, min_loc5, max_loc5 = cv2.minMaxLoc(res5)
        if max_val3 >= threshold:
            set_paused(2)
            hook.send("<@&1380790894248202282> POLO PORTAL")
            print("POLO\nPOLO\nPOLO\nPOLO\nPOLO\n")
        elif max_val4 >= threshold:
            set_paused(2)
            hook.send("<@&1380790894248202282> VIOLETTA")
            print("VIOLETTA\nVIOLETTA\nVIOLETTA\nVIOLETTA\nVIOLETTA")
        elif max_val5 >= threshold:
            set_paused(2)
            hook.send("<@&1380790894248202282> DIED")
            print("DIED\nDIED\nDIED\nDIED\nDIED")
        else:
            print("safe")

def beep():
    print("\a")

def set_paused(state):
    global paused_state
    with status_lock:
        paused_state = state
        if state == 0:
            pause_event.set()
            status_queue.put("Status: Running")
            beep()
        elif state == 1:
            pause_event.clear()
            status_queue.put("Status: Paused")
            beep()
        elif state == 2:
            pause_event.clear()
            status_queue.put("Status: Stopped")
            beep()
            hook.send("<@&1380790894248202282> bot stopped, please check")
            time.sleep(1.5)
            beep()
            time.sleep(1.5)
            beep()

def start_gui():
    def pause():
        set_paused(1)
        status_label.config(text="Status: Paused")
        signal_canvas.itemconfig(signal_light, fill="orange")

    def resume():
        set_paused(0)
        status_label.config(text="Status: Running")
        signal_canvas.itemconfig(signal_light, fill="green")

    def poll_status():
        try:
            while True:
                status = status_queue.get_nowait()
                status_label.config(text=status)
                if "Stopped" in status:
                    signal_canvas.itemconfig(signal_light, fill="red")
                elif "Paused" in status:
                    signal_canvas.itemconfig(signal_light, fill="orange")
                else:
                    signal_canvas.itemconfig(signal_light, fill="green")
        except queue.Empty:
            pass
        root.after(100, poll_status)

    root = tk.Tk()
    root.title("Control Panel")
    root.attributes('-topmost', True)
    root.geometry("800x200")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    controls_frame = tk.Frame(main_frame)
    controls_frame.pack(side="left", fill="y", padx=20, pady=20)

    pause_button = tk.Button(controls_frame, text="Pause", command=pause, width=20, height=1, font=('Times 18'))
    pause_button.pack(pady=5)
    resume_button = tk.Button(controls_frame, text="Resume", command=resume, width=20, height=1, font=('Times 18'))
    resume_button.pack(pady=5)
    status_label = tk.Label(controls_frame, text="Status: Running",font=('Times 18'))
    status_label.pack(pady=5)

    signal_canvas = tk.Canvas(main_frame, width=600, height=200, highlightthickness=0)
    signal_canvas.pack(side="right", padx=20, pady=20)
    signal_light = signal_canvas.create_rectangle(0, 0, 600, 200, fill="green",)

    root.after(100, poll_status)
    root.mainloop()

def main():
    hook.send("<@&1380790894248202282> STARTING BOT")
    gui_thread = threading.Thread(target=start_gui, daemon=True)
    gui_thread.start()
    #kb_thread = threading.Thread(target=keyboard_listener, daemon=True)
    #kb_thread.start()
    while True:
        lie()
        pause_event.wait()  # Wait here if paused
        maps.sunless_area()

if __name__ == '__main__':
    main()