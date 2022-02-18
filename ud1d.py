import keyboard as key
import time
import pyautogui
from PIL import ImageGrab
import os

def main():
    cmd = 'C:/ud1d/speak_script.sh '
    while True:
        if key.is_pressed('q'):
            os.system(cmd+'เสร็จแล้วจ้า')
            break
        mouse_pos = pyautogui.position()
        x = mouse_pos.x
        y = mouse_pos.y
        screen = ImageGrab.grab()
        color = screen.getpixel((x, y))
        print(color)
        time.sleep(0.05)
        
    '''
    count = 0
    loop count < 5
        loop
            get color in record button
            if ready
                break
            sleep 0.1 sec.
        click record button
        wait 10 sec.
        loop
            get color in save button
            if ready
                break
            sleep 0.1 sec.
        click save button
        loop
            get color in record button
            if ready
                count++
            sleep 2 sec.
    play finished sound.
    '''
    
if __name__ == "__main__":
    main()
