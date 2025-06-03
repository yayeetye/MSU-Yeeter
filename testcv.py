import cv2
import numpy as np
import pytesseract
import pyautogui

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Take screenshot and convert to OpenCV format
#screenshot = pyautogui.screenshot()
screenshot = cv2.imread("violet.png")
img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
cv2.imwrite('lie2.jpg', img)
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
print(text)

if "Lie Detector" in text:
    print("yes")

