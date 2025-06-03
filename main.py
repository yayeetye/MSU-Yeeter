import cv2
import numpy as np
import pyautogui
import pydirectinput as pdi
import time
import tkinter as tk
import threading
import random
import pytesseract

import queue

import rune_solver
import pot

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#threading
pause_event = threading.Event()
pause_event.set()
status_queue = queue.Queue()
paused_state = 0
status_lock = threading.Lock()

auto = True
GTDELAY = 3
times = 0
last_buff = 0
# Define the region of the minimap (left, top, width, height)
MINIMAP_REGION = (0,0,400,400)  # <-- You must specify these based on your screen!
POT_HP,MIN_HP = 50,30
POT_MP,MIN_MP = 20,10
BUTTON_MP,BUTTON_HP = 'j','h'
# Load the template (yellow marker)
char = cv2.imread('yellow_marker_720.PNG', cv2.IMREAD_UNCHANGED)
runepic = cv2.imread('rune.PNG', cv2.IMREAD_UNCHANGED)
polo = cv2.imread('polo.PNG', cv2.IMREAD_UNCHANGED)
violet = cv2.imread('violet.PNG', cv2.IMREAD_UNCHANGED)

if char is None:
    raise FileNotFoundError("yellow_marker.PNG not found")
if runepic is None:
    raise FileNotFoundError("rune.PNG not found")
if polo is None:
    raise FileNotFoundError("rune.PNG not found")
if violet is None:
    raise FileNotFoundError("violet.PNG not found")

if char.shape[2] == 4:  # Has alpha channel
    char = cv2.cvtColor(char, cv2.COLOR_BGRA2BGR)
if runepic.shape[2] == 4:  # Has alpha channel
    runepic = cv2.cvtColor(runepic, cv2.COLOR_BGRA2BGR)
if polo.shape[2] == 4:  # Has alpha channel
    polo = cv2.cvtColor(polo, cv2.COLOR_BGRA2BGR)
if violet.shape[2] == 4:  # Has alpha channel
    violet = cv2.cvtColor(violet, cv2.COLOR_BGRA2BGR)

def capture_minimap():
    screenshot = pyautogui.screenshot(region=MINIMAP_REGION)
    minimap_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return minimap_img

def find_marker_location():
    minimap_img = capture_minimap()
    # Ensure both minimap_img and template are BGR and uint8
    if minimap_img.shape[2] != 3:
        minimap_img = minimap_img[:, :, :3]  # Drop alpha if somehow present
    res = cv2.matchTemplate(minimap_img, char, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    threshold = 0.8
    if max_val >= threshold:
        marker_pos = max_loc
        print(f"Marker found at: {marker_pos}")

        res2 = cv2.matchTemplate(minimap_img, runepic, cv2.TM_CCOEFF_NORMED)
        min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
        if max_val2 >= threshold:
            rune_pos = max_loc2
            print(f"RUNE found at: {rune_pos}")
            return marker_pos, rune_pos
        else:
            return marker_pos, None
    else:
        print("Marker not found")
        return None, None

def go_to(destx):
    print(f"Moving to: {destx}")
    character, rune = find_marker_location()
    if character[0] - destx > 2:
        pdi.keyDown('left')
        while True:
            character, rune = find_marker_location()
            if character[0] - destx < GTDELAY:
                pdi.keyUp('left')
                break
    elif character[0] - destx > 0:
        pdi.press('left')
    elif character[0] - destx < -2:
        pdi.keyDown('right')
        while True:
            character, rune = find_marker_location()
            if character[0] - destx > -1*GTDELAY:
                pdi.keyUp('right')
                break
    else:
        pdi.press('right')

def buff(key,duration,confirm=False):
    global last_buff
    current_ime = time.time()
    if last_buff == 0 or time.time() - last_buff > duration:
        pdi.press(key)
        if confirm == True:
            pdi.press('right')
            pdi.press('enter')
        last_buff = time.time()

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
    cv2.imwrite('lie.jpg', mask)

    if "Lie Detector" in text:
        set_paused(2)
        print("CAPTCHA\nCAPTCHA\nCAPTCHA\nCAPTCHA\nCAPTCHA")
    else:
        threshold = 0.8
        res3 = cv2.matchTemplate(img, polo, cv2.TM_CCOEFF_NORMED)
        min_val3, max_val3, min_loc3, max_loc3 = cv2.minMaxLoc(res3)

        res4 = cv2.matchTemplate(img, violet, cv2.TM_CCOEFF_NORMED)
        min_val4, max_val4, min_loc4, max_loc4 = cv2.minMaxLoc(res4)
        if max_val3 >= threshold:
            set_paused(2)
            print("POLO\nPOLO\nPOLO\nPOLO\nPOLO\n")
        elif max_val4 >= threshold:
            set_paused(2)
            print("VIOLETTA\nVIOLETTA\nVIOLETTA\nVIOLETTA\nVIOLETTA")
        else:
            print("safe")

def beep():
    print("\a")

def sunless_area():
    global times
    pt0 = 101
    pt1 = 112
    pt2 = 123
    pt3 = 142
    marker_pos, rune_pos = find_marker_location()
    if marker_pos == None:
        print("no character position")
        time.sleep(5)
        return
    if rune_pos == None:
        print("no rune")
        rune_pos = [1000,1000]

    hp = pot.get_hp()
    print(f"HP: {hp:.2f}%")
    mp = pot.get_mp()
    print(f"MP: {mp:.2f}%")
    chance = random.random()
    #use hp pot
    if hp < POT_HP and chance < 0.15:
        pdi.press(BUTTON_HP)
    elif hp < MIN_HP:
        pdi.press(BUTTON_HP)
    # use mp pot
    if mp < POT_MP and chance < 0.15:
        pdi.press(BUTTON_MP)
    elif mp < MIN_MP:
        pdi.press(BUTTON_MP)

    buff('o',80)
    if auto == False:
        time.sleep(1)
        print("Auto = False")
    elif marker_pos[1] < pt1+1:  # 1st platform (top portal)
        times = 0
        pdi.keyDown('right')
        pdi.press('x')
        time.sleep(0.6)
        pdi.keyUp('right')
        time.sleep(0.2)
        if rune_pos[1] < pt1+1:
            print("case0")
            go_to(rune_pos[0])
            rune_solver.rune_break()

    elif marker_pos[1] < pt2+2 and marker_pos[0] < 110 : #platform 2 left side
        pdi.keyDown('right')
        pdi.press('space')
        pdi.press('space')
        pdi.press('x')
        pdi.keyUp('right')
        time.sleep(0.3)
        pdi.press('x')
        time.sleep(0.3)
        pdi.press('left')
        pdi.press('x')
        time.sleep(0.3)
        if rune_pos[1] < pt2+2 and rune_pos[0] < 110 and rune_pos[1] > pt1:
            print("case1")
            go_to(rune_pos[0])
            rune_solver.rune_break()
        if rune_pos[1] < pt0+1:
            print("case2")
            pdi.press('v')
            time.sleep(3)
            go_to(rune_pos[0])
            rune_solver.rune_break()
    elif marker_pos[1] < pt2: #platform 2 right side
        pdi.keyDown('down')
        pdi.press('space')
        time.sleep(0.1 + random.random() * 0.1)
        pdi.keyUp('down')
        if rune_pos[1] < pt2 and rune_pos[0] > 110 and rune_pos[1] > pt1:
            print("case3")
            go_to(rune_pos[0])
            rune_solver.rune_break()
    elif marker_pos[1] < pt3-2 and marker_pos[0] == 134: #ladder rightmost
        pdi.keyDown('right')
        pdi.press('space')
        pdi.keyUp('right')
    elif marker_pos[1] < pt3+6: #last platform
        if rune_pos[1] < pt3+6 and rune_pos[1] > pt2+3:
            print("case4")
            go_to(rune_pos[0])
            rune_solver.rune_break()
        if rune_pos[1] < pt2 and rune_pos[0] > 110 and marker_pos[0] > 110:
            print("case5")
            time.sleep(1)
            pdi.press('v')
            time.sleep(3)
            go_to(rune_pos[0])
            rune_solver.rune_break()
        if times == 0:
            if marker_pos[0] > 90:
                pdi.press('left')
                pdi.press('x')
                time.sleep(0.4)
                pdi.press('space')
                pdi.press('space')
            elif chance < 0.1:
                pdi.press('space')
                pdi.press('space')
                time.sleep(0.4)
                pdi.press('space')
                pdi.press('space')
                time.sleep(0.4)
                pdi.press('right')
                pdi.press('x')
                time.sleep(0.4)
                pdi.press('space')
                pdi.press('space')
                times = 1
            else:
                times = 1
        else:
            if marker_pos[0] == 87:
                pdi.press('up')
                return
            pdi.press('left')
            pdi.press('x')
            time.sleep(0.3 + random.random() * 0.1)
            pdi.press('up')
            pdi.press('right')
            pdi.press('x')
            time.sleep(0.3 + random.random() * 0.1)
            if marker_pos[0] == 87 or marker_pos[0] == 86 or marker_pos[0] == 88:
                pdi.press('up')
            else:
                go_to(87)

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
            time.sleep(1)
            beep()
            time.sleep(1)
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
'''
def keyboard_listener():
    global paused_state
    while True:
        if keyboard.is_pressed('l'):
            with status_lock:
                if paused_state == 2:
                    new_state = 0
                elif paused_state == 0:
                    new_state = 1
                else:  # paused_state == 1
                    new_state = 0
            set_paused(new_state)
            while keyboard.is_pressed('l'):
                time.sleep(0.1)  # Debounce'''

def main():
    gui_thread = threading.Thread(target=start_gui, daemon=True)
    gui_thread.start()
    #kb_thread = threading.Thread(target=keyboard_listener, daemon=True)
    #kb_thread.start()
    while True:
        lie()
        pause_event.wait()  # Wait here if paused
        sunless_area()

if __name__ == '__main__':
    main()