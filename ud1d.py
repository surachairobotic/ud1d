import pyautogui
from PIL import ImageGrab
import time

class UD1D():
    def __init__(self):
        self.rec_pos = pyautogui.Point(1204, 479)
        self.sav_pos = pyautogui.Point(  72, 480)
        self.rec_active = (230, 188, 93)
        self.rec_notactive = (210, 210, 210)
        self.sav_enable = (210, 210, 210)
        self.sav_disable = (232, 232, 232)

    def rec_click(self):
        print("rec click.")
        self.mouse_click(self.rec_pos.x, self.rec_pos.y)
    def sav_click(self):
        print("sav click.")
        self.mouse_click(self.sav_pos.x, self.sav_pos.y)

    def rec_status(self):
        color = self.btn_status(self.rec_pos.x, self.rec_pos.y)
        if color == self.rec_active:
            return 1
        elif color == self.rec_notactive:
            return 0
        else:
            print("incorrect color on rec_status. : " + str(color))
            return -1

    def sav_status(self):
        color = self.btn_status(self.sav_pos.x, self.sav_pos.y)
        if color == self.sav_enable:
            return 1
        elif color == self.sav_disable:
            return 0
        else:
            print("incorrect color on sav_status. : " + str(color))
            return -1

    def mouse_click(self, x, y, clicks=1):
        pyautogui.click(x, y, clicks)
    def mouse_doubleclick(self, x, y):
        pyautogui.doubleClick(x, y)

    def btn_status(self, x, y):
        screen = ImageGrab.grab()
        color = screen.getpixel((x, y))
        return color

    def set_file_name(self, fname):
        self.mouse_click(86, 166)
        for i in range(10):
            pyautogui.press('up')
            time.sleep(0.01)
        pyautogui.keyDown('shift')
        for i in range(10):
            pyautogui.press('down')
            time.sleep(0.01)
        pyautogui.keyUp('shift')
        pyautogui.press('backspace')
        pyautogui.write(fname)