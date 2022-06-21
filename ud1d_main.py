import keyboard as key
import time, math, sys
import os
from gtts import gTTS

from pprint import pprint
import keyboard as key
import time
import matplotlib.pyplot as plt

from robot import Robot
from ud1d import UD1D

import pyautogui
from PIL import ImageGrab

def tts(text):
    obj = gTTS(text=text, lang='th', slow=False)
    obj.save("welcome.mp3")
    os.system("vlc --play-and-exit welcome.mp3")

def callbackOutMotionEnd(res, user):
    print("RES : " + str(res))
    print("USER : " + str(user))

def main(state, fname):
    print("Start")
    offset=0
    angle = 0
    if fname.find('angleA') != -1:
        angle = 0
    elif fname.find('angleB') != -1:
        indx = fname.find('angleB')
        angle = int(fname[indx+6:indx+8])

    robot = Robot()
    if state == 'on':
        print("Robot init : {}".format(robot.init(True)))
        robot.Servo(True)
        #robot.moveAlign(0, 90-angle)
        exit()
    elif state == 'off':
        print("Robot init : {}".format(robot.init(True)))
        robot.Servo(False)
        exit()
    elif state == '0':
        print("Robot init : {}".format(robot.init(True)))

        robot.Origin(3)
        robot.Jog('UP')
        robot.Inching('DOWN')
        robot.Inching('DOWN')
        robot.Origin(2)
        robot.Jog('FRONT')
        robot.Origin(1)
        robot.Jog('FAR')
        print("ok")
        exit()
    elif state == '1':
        print("Robot init : {}".format(robot.init(True)))
        robot.Jog('UP')
        robot.Inching('DOWN')
        robot.Inching('DOWN')
        robot.Jog('FRONT')
        robot.Jog('FAR')
        exit()
    elif state == '2':
        print("Robot init : {}".format(robot.init(True)))
    elif state == '3':
        print("Robot init : {}".format(robot.init(True)))
        x = []
        y = []
        for i in range(35):
            kx, ky = robot.moveAlign(i*10, 90-angle)
            x.append(kx)
            y.append(ky)
        plt.xlim([0, 450])
        plt.ylim([0, 350])
        plt.plot(x, y)
        plt.show()
        exit()

    ud1d = UD1D()
    #tts("เริ่มเก็บข้อมูล")
    recTime = 10
    step = 4
    count = 1
    while count <= 35:
        robot.Servo(True)
        time.sleep(0.5)
        #robot.moveDist(count)
        robot.moveAlign((count-1)*10, 90-angle)
        time.sleep(0.5)
        robot.Servo(False)
        #time.sleep(2)
        #tts("รอบที่ " + str(count))
        while True:
            status = ud1d.rec_status()
            if status == 0:
                break
            print("rec_status is active. : " + str(status))
            time.sleep(0.1)
        print("rec_status is'n active. will click record button in 0.5 sec.")
        time.sleep(0.5)
        while True:
            ud1d.rec_click()
            status = ud1d.rec_status()
            if status == 1:
                break
        ud1d.set_file_name(fname+str(count+offset))
        time.sleep(recTime-2)
        while ud1d.sav_status() != 1:
            print("sav_status is disable.")
            time.sleep(0.1)
        print("sav_status is'n active. will click record button in 0.5 sec.")
        time.sleep(0.5)
        ud1d.sav_click()
        robot.Servo(True)
        while True:
            status = ud1d.rec_status()
            if status == 0:
                break
            print("rec_status is active : " + str(status))
            time.sleep(1)
        print("rec_status is ready. finished.")
        count = count+step
        step=5
    robot.moveAlign(0, 90-angle)
    robot.Disconnect()
    tts("เสร็จแล้วจ้า")

def test1():
    cmd = 'C:/ud1d/speak_script.sh '
    while True:
        if key.is_pressed('q'):
            #os.system(cmd+'เสร็จแล้วจ้า')
            break
        mouse_pos = pyautogui.position()
        x = mouse_pos.x
        y = mouse_pos.y
        x = 1204
        y = 479
        screen = ImageGrab.grab()
        color = screen.getpixel((x, y))
        
        print(str(time.time()) + " : " + "pos=" + str(mouse_pos) + ", color=" + str(color) + ", type(mouse)=" + str(type(mouse_pos)) + ", type(color)=" + str(type(color)))
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
def testRobot(state):
    robot = Robot()
    if state == 'on':
        print("Robot init : {}".format(robot.init(True)))
        robot.Servo(True)
        #robot.moveAlign(0, 90-angle)
        exit()
    elif state == 'off':
        print("Robot init : {}".format(robot.init(True)))
        robot.Servo(False)
        exit()
    elif state == '0':
        print("Robot init : {}".format(robot.init(True)))

        robot.Origin(3)
        robot.Jog('UP')
        robot.Inching('DOWN')
        robot.Inching('DOWN')
        robot.Origin(2)
        robot.Jog('FRONT')
        robot.Origin(1)
        robot.Jog('FAR')
        print("ok")
        exit()
    elif state == '1':
        print("Robot init : {}".format(robot.init(True)))
        robot.Jog('UP')
        robot.Inching('DOWN')
        robot.Inching('DOWN')
        robot.Jog('FRONT')
        robot.Jog('FAR')
        exit()
    elif state == '2':
        print("Robot init : {}".format(robot.init(True)))
    elif state == '3':
        print("Robot init : {}".format(robot.init(True)))
        x = []
        y = []
        for i in range(35):
            kx, ky = robot.moveAlign(i*10, 90-angle)
            x.append(kx)
            y.append(ky)
        plt.xlim([0, 450])
        plt.ylim([0, 350])
        plt.plot(x, y)
        plt.show()
        exit()


if __name__ == "__main__":
    print('Number of arguments: {}'.format(len(sys.argv)))
    print('Argument(s) passed: {}'.format(str(sys.argv[1])))

    testRobot('on')

    #test1()
    #if sys.argv[1] == '2' and len(sys.argv) >= 3:
    #    fname = sys.argv[2]

    '''
    names = ['bar80_flow4_angleA45_dist', 'bar80_flow4_angleB45_dist']
    for i in range(len(names)):
        main(str(sys.argv[1]), names[i])
    '''