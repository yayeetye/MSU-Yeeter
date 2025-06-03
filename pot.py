# screen_number_reader.py
import cv2
import numpy as np
from PIL import ImageGrab
import time

# Optional: set this if tesseract is not in PATH
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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


if __name__ == '__main__':
    while True:
        hp = get_hp()
        print(f"Red area: {hp:.2f}%")
        mp = get_mp()
        print(f"Blue area: {mp:.2f}%")
        time.sleep(2)