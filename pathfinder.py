import numpy as np
import pyautogui
import asyncio
import time

import sys
sys.path.append('.')  # So you can import from map.py in this directory
from map import find_marker_location

MAP_PATH = "map_reconstruction.npy"
WAYPOINT_TOLERANCE = 6  # pixels

def load_path(filename, n=20):
    data = np.load(filename, allow_pickle=True)
    return [tuple(x) for x in data[:n]]

async def wait_marker():
    location = None
    while location is None:
        location = await find_marker_location()
    return location

async def move_to_waypoint(target, mode='platform'):
    '''Move toward the (x, y) pixel on the minimap.'''
    print(f"Moving toward: {target}")
    while True:
        pos = await find_marker_location()
        if not pos:
            print("Marker not found. Retrying...")
            await asyncio.sleep(0.05)
            continue
        cx, cy = pos
        tx, ty = target
        dx, dy = tx - cx, ty - cy
        done = abs(dx) <= WAYPOINT_TOLERANCE and abs(dy) <= WAYPOINT_TOLERANCE

        if done:
            pyautogui.keyUp('left'); pyautogui.keyUp('right')
            break

        if abs(dx) > WAYPOINT_TOLERANCE:
            if dx > 0:
                pyautogui.keyUp('left')
                pyautogui.keyDown('right')
            else:
                pyautogui.keyUp('right')
                pyautogui.keyDown('left')
        else:
            # X is in place, release both keys.
            pyautogui.keyUp('left'); pyautogui.keyUp('right')

        # Jump if needed
        if mode == 'jump' and dy < -WAYPOINT_TOLERANCE and abs(dx) < 16:
            pyautogui.keyDown('space')
            time.sleep(0.15)
            pyautogui.keyUp('space')
            await asyncio.sleep(0.1)

        await asyncio.sleep(0.04)

    pyautogui.keyUp('left'); pyautogui.keyUp('right')

async def main():
    print("Loading path...")
    path = load_path(MAP_PATH)
    print("Focus the game window! Starting in 2 seconds...")
    await asyncio.sleep(2)

    for i, point in enumerate(path[1:], 1):
        target = point[:2]
        label = point[2] if len(point) > 2 else "platform"
        print(f"Step {i}/{len(path)-1} → Mode: {label}")
        await move_to_waypoint(target, mode=label)
        await asyncio.sleep(0.12)  # brief pause between points

    print("Path complete.")

if __name__ == '__main__':
    asyncio.run(main())
