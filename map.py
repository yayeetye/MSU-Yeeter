import cv2
import numpy as np
import pyautogui
import pydirectinput as pdi
import asyncio
import time

#increase 3rd platform find portal efficiency
#fix stuck at ladder issue
#add neso collection
auto = True
# Define the region of the minimap (left, top, width, height)
MINIMAP_REGION = (0,0,400,400)  # <-- You must specify these based on your screen!

# Load the template (yellow marker)
template = cv2.imread('yellow_marker_720.PNG', cv2.IMREAD_UNCHANGED)
if template is None:
    raise FileNotFoundError("yellow_marker.PNG not found")

if template.shape[2] == 4:  # Has alpha channel
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)

async def capture_minimap():
    screenshot = pyautogui.screenshot(region=MINIMAP_REGION)
    minimap_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return minimap_img

async def find_marker_location():
    minimap_img = await capture_minimap()
    # Ensure both minimap_img and template are BGR and uint8
    if minimap_img.shape[2] != 3:
        minimap_img = minimap_img[:, :, :3]  # Drop alpha if somehow present
    res = cv2.matchTemplate(minimap_img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    threshold = 0.8
    if max_val >= threshold:
        marker_pos = max_loc
        print(f"Marker found at: {marker_pos}")
        print(marker_pos[1])
        if auto == False:
            time.sleep(0.5)
            print("Auto False")
        elif marker_pos[1] < 104: #1st platform
            pdi.press('left')
            pdi.press('x')
            time.sleep(0.5)
            pdi.press('right')
            pdi.press('x')
            time.sleep(0.5)
            pdi.keyDown('down')
            pdi.press('space')
            time.sleep(0.1)
            pdi.keyUp('down')
            times =   0

        elif marker_pos[1] < 123: #ladder
            pdi.keyDown('left')
            pdi.press('space')
            pdi.keyUp('left')

        elif marker_pos[1] < 127: #2nd platform
            pdi.press('left')
            pdi.press('x')
            time.sleep(0.5)
            pdi.press('right')
            pdi.press('x')
            time.sleep(0.5)
            pdi.keyDown('down')
            pdi.press('space')
            time.sleep(0.1)
            pdi.keyUp('down')

        elif marker_pos[1] < 145: #ladder
            pdi.keyDown('left')
            pdi.press('space')
            pdi.keyUp('left')

        elif marker_pos[1] < 149: #3rd platform
            if marker_pos[0] == 95 or marker_pos[0] == 96:
                pdi.press('up')
            pdi.press('left')
            pdi.press('x')
            time.sleep(0.5)
            pdi.press('right')
            pdi.press('x')x
            time.sleep(0.5)
            if marker_pos[0] < 95:
                dist = 95 - marker_pos[0]
                if dist > 25:
                    pdi.press('right')
                    pdi.press('space')
                    pdi.press('space')
                else:
                    pdi.keyDown('right')
                    time.sleep(0.1*dist)
                    pdi.keyUp('right')
                times = 1

            elif marker_pos[0] > 95:
                dist = marker_pos[0] - 95
                if dist > 25:
                    pdi.press('left')
                    pdi.press('space')
                    pdi.press('space')
                else:
                    pdi.keyDown('left')
                    time.sleep(0.1*dist)
                    pdi.keyUp('left')
                times = 1

        return marker_pos
    else:
        print("Marker not found")
        return None


async def main_loop():
    while True:
        await find_marker_location()
        await asyncio.sleep(0.2)  # Adjust the polling rate as needed


if __name__ == '__main__':
    asyncio.run(main_loop())