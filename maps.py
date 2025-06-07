import cv2
import numpy as np
from PIL import ImageGrab
import time
import pyautogui
import random
import pydirectinput as pdi
import rune_solver

# Optional: set this if tesseract is not in PATH
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe"

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
char = cv2.imread('pic\\yellow_marker_720.PNG', cv2.IMREAD_UNCHANGED)
runepic = cv2.imread('pic\\rune.PNG', cv2.IMREAD_UNCHANGED)
polo = cv2.imread('pic\\polo.PNG', cv2.IMREAD_UNCHANGED)
violet = cv2.imread('pic\\violet.PNG', cv2.IMREAD_UNCHANGED)

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

def buff(key,duration,confirm=False):
    global last_buff
    if last_buff == 0 or time.time() - last_buff > duration:
        pdi.press(key)
        if confirm == True:
            pdi.press('right')
            pdi.press('enter')
        last_buff = time.time()

def go_to(destx):
    print(f"Moving to: {destx}")
    character, rune = find_marker_location()
    if character == None:
        print("no character position")
        time.sleep(1)
        return

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

def get_hp():
    # Capture the screen or a region
    region = (530, 708, 696, 709)
    img = ImageGrab.grab(bbox=region)
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    cv2.imwrite('screen.jpg', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red can wrap around the hue, so use two ranges
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    red_pixels = cv2.countNonZero(mask)
    total_pixels = mask.size
    percent_red = (red_pixels / total_pixels) * 100
    return percent_red

def get_mp():
    # Capture the screen or a region
    region = (530, 723, 696, 724)
    img = ImageGrab.grab(bbox=region)
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    cv2.imwrite('screen.jpg', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red can wrap around the hue, so use two ranges
    lower_blue1 = np.array([0, 0, 0])
    upper_blue1 = np.array([140, 250, 150])

    mask = cv2.inRange(hsv, lower_blue1, upper_blue1)


    red_pixels = cv2.countNonZero(mask)
    total_pixels = mask.size
    percent_red = 100-(red_pixels / total_pixels) * 100
    return percent_red

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
        rune_pos = [1000, 1000]
    hp = get_hp()
    print(f"HP: {hp:.2f}%")
    mp = get_mp()
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
        if rune_pos[1] < pt2 and rune_pos[0] > 110 and rune_pos[1] > pt1:
            print("case3")
            go_to(rune_pos[0])
            rune_solver.rune_break()
        pdi.keyDown('down')
        pdi.press('space')
        time.sleep(0.1 + random.random() * 0.1)
        pdi.keyUp('down')
    elif marker_pos[1] < pt3-2 and marker_pos[0] == 134: #ladder rightmost
        pdi.keyDown('right')
        pdi.press('space')
        pdi.keyUp('right')
    elif marker_pos[1] < pt3+6: #last platform
        if rune_pos[1] < pt3+6 and rune_pos[1] > pt2+3:
            print("case4")
            go_to(rune_pos[0])
            rune_solver.rune_break()
        elif rune_pos[1] < pt2 and rune_pos[0] > 110 and marker_pos[0] > 110:
            print("case5")
            time.sleep(1)
            pdi.press('v')
            time.sleep(1)
        elif times == 0:
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
