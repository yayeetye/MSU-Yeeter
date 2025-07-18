import ctypes
from ctypes import wintypes
import time as t
import random


user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
MAPVK_VK_TO_VSC = 0
# msdn.microsoft.com/en-us/library/dd375731
wintypes.ULONG_PTR = wintypes.WPARAM
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))
LPINPUT = ctypes.POINTER(INPUT)
def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
def F12():
    PressKey(0x7B)
    t.sleep(0.2)
    ReleaseKey(0x7B)
    # you can change 0x30 to any key you want. For more info look at :
    # msdn.microsoft.com/en-us/library/dd375731

def up():
    PressKey(0x26)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0x26)

def right():
    PressKey(0x27)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0x27)

def down():
    PressKey(0x28)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0x28)

def left():
    PressKey(0x25)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0x25)

def y():
    PressKey(0x59)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0x59)

def alt():
    PressKey(0xA4)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0xA4)

def v():
    PressKey(0x56)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0x56)


def x():
    PressKey(0x58)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0x58)


def space():
    PressKey(0x20)
    t.sleep(random.uniform(0.15, 0.25))
    ReleaseKey(0x20)

function_map = {"up": up, "down": down, "left": left, "right": right }