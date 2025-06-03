import cv2
import numpy as np
import pyautogui
import asyncio
import keyboard  # pip install keyboard
import os

MINIMAP_REGION = (0, 0, 400, 400)  # Set this for your game!
TEMPLATE_PATH = "yellow_marker_720.PNG"
FILENAME = "map_reconstruction.npy"

# Ensure both screenshot and template are 3-channel BGR
template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_UNCHANGED)
if template is None:
    raise FileNotFoundError(f"{TEMPLATE_PATH} not found")
if template.shape[2] == 4:
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)

locations = []  # (x, y, label) tuples

async def capture_minimap():
    screenshot = pyautogui.screenshot(region=MINIMAP_REGION)
    minimap_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    if minimap_img.shape[2] == 4:
        minimap_img = minimap_img[:, :, :3]
    return minimap_img

async def find_marker_location():
    minimap_img = await capture_minimap()
    res = cv2.matchTemplate(minimap_img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.8:
        print(max_loc)
        return max_loc
    return None

async def record_path(label):
    print(f"Recording path labeled: {label}. Press 'q' to stop.")
    while not keyboard.is_pressed('q'):
        marker = await find_marker_location()
        if marker:
            locations.append((*marker, label))
            print(f"Recorded: {marker} as {label}")
        await asyncio.sleep(0.05)  # Adjust as needed
    print("Recording stopped.")

async def main():
    print("Get ready. You can record multiple elements by calling record_path with different labels.")
    await asyncio.sleep(2)
    # Example: record a platform
    await record_path("jump")
    # Optionally: record more elements like ladders
    # await record_path("ladder")
    # Save the data
    if os.path.exists(FILENAME):
        all_points = np.load(FILENAME, allow_pickle=True).tolist()
    else:
        all_points = []

    # `locations` is your new (x, y, label) list for this run
    all_points.extend(locations)

    # Save the combined list back to file
    np.save(FILENAME, np.array(all_points, dtype=object))

    print(f"Saved {len(locations)} points to map_reconstruction.npy")
    print(f"Saved {len(all_points)} total points to {FILENAME}")


if __name__ == '__main__':
    asyncio.run(main())
