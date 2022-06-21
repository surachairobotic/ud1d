from pprint import pprint
import keyboard as key
import time, math

import clr
clr.AddReference('C:\\Program Files (x86)\\Yamaha Motor\\RCX3-SDK\\bin\\RCX3CLI.dll')

# #use this section of code for troubleshooting
# from clr import System
# from System import Reflection
# full_filename = r'C:\\Program Files (x86)\\Yamaha Motor\\RCX3-SDK\\bin\\RCX3CLI.dll'
# Reflection.Assembly.LoadFile(full_filename)   #this elaborate the error in details

from RCX3DOTNET import CRCX3
import RCX3DOTNET

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))


def main():
    p90 = math.pi/2
    p45 = math.pi/4
    p30 = math.pi/6
    p15 = math.pi/12

    theta = 90-15
    theta = theta / 180.0 * math.pi
    x = []
    y = []
    for i in range(1, 36):
        x.append(450-(i*10*math.cos(theta)))
        y.append(350-(i*10*math.sin(theta)))
    print(x)
    print(y)

    m_RCX3 = CRCX3.Create()

    m_RCX3.Host = "192.168.0.2"
    m_RCX3.Port = 23

    if m_RCX3.Connect():
        print("RCX3 : Connected.")
        msg = m_RCX3.Controller[1].Version
        print("Controller Version : " + str(msg.Major) + "." + str(msg.Minor) + " rev." + str(msg.Revision))
        msg = m_RCX3.Controller[1].PLDVersion
        print("PLD Version : " + str(msg.Major) + "." + str(msg.Minor) + " rev." + str(msg.Revision))
        msg = m_RCX3.Controller[1].DriverVersion[1]
        print("Driver Version : " + str(msg.Major) + "." + str(msg.Minor) + " rev." + str(msg.Revision))
        #89
    else:
        print("RCX3 : Failed to connect.")
        exit()


    m_RCX3.Power = True
    m_RCX3.Servo = True
    #m_RCX3.Power = False
    #m_RCX3.Servo = False


    '''
    m_RCX3.Robot[robotNo].Brake = false;
    m_RCX3.Robot[robotNo].Servo = false;
    m_RCX3.Robot[robotNo].Axis[axisNo].Servo = false;
    m_RCX3.Robot[robotNo].Axis[axisNo].Brake = false;
    '''

    #dump(m_RCX3.Robot)

    m_RCX3.Robot[1].AutoSpeed = 50
    m_RCX3.Robot[1].Speed = 20
    m_RCX3.Robot[1].ManualSpeed = 20
    m_RCX3.Robot[1].InchingDistance = 10000

    m_RCX3.Robot[1].Axis[1].PushSpeed = 50
    m_RCX3.Robot[1].Axis[2].PushSpeed = 50
    m_RCX3.Robot[1].Axis[3].PushSpeed = 50

    #m_RCX3.Robot[1].Origin(RCX3DOTNET.EAxisType.ALL_TYPES)
    cnt=0
    # Robot[1].Jog(1, 2, 3) = [ base[+Far:, -:Near], mid[+Front:, -:Back], tip[+Down, -Up]
    #m_RCX3.Robot[1].Jog(1, RCX3DOTNET.EMoveDirection.PLUS)
    mode = 'i'
    axis = 2
    t = time.time()
    while True:
        if key.is_pressed('q'):
            break
        elif key.is_pressed('ESC'):
            m_RCX3.Stop()
        if time.time()-t > 1.0:
            if key.is_pressed('p'):
                xx = [m_RCX3.Robot[1].Position.Axis[0], m_RCX3.Robot[1].Position.Axis[1], m_RCX3.Robot[1].Position.Axis[2]]
                print(xx)
                # msg = pos2dist(m_RCX3.Robot[1].Position.Axis[1])
                # print(msg)
                t = time.time()
            elif key.is_pressed('1'):
                m_RCX3.Robot[1].Axis[1].Move(0.0)
            elif key.is_pressed('2'):
                m_RCX3.Robot[1].Axis[1].Move(450.0)
            elif key.is_pressed('3'):
                m_RCX3.Robot[1].Axis[2].Move(0.0)
            elif key.is_pressed('4'):
                m_RCX3.Robot[1].Axis[2].Move(350.0)
            elif key.is_pressed('5'):
                aaa = [cnt, x[cnt], y[cnt]]
                print(aaa)
                m_RCX3.Robot[1].Axis[2].Move(y[cnt])
                time.sleep(1)
                m_RCX3.Robot[1].Axis[1].Move(x[cnt])
                cnt=(cnt+1)%len(x)
                t = time.time()
            elif key.is_pressed('i'):
                mode = 'i'
                t = time.time()
            elif key.is_pressed('j'):
                mode = 'j'
                t = time.time()
            elif key.is_pressed('1'):
                axis = 1
                t = time.time()
            elif key.is_pressed('2'):
                axis = 2
                t = time.time()
            elif key.is_pressed('3'):
                axis = 3
                t = time.time()
            elif key.is_pressed('w') or key.is_pressed('s'):
                print(mode + ' : ' + str(axis))
                direction = RCX3DOTNET.EMoveDirection.PLUS
                if key.is_pressed('s'):
                    direction = RCX3DOTNET.EMoveDirection.MINUS
                if mode == 'i':
                    m_RCX3.Robot[1].Inching(axis, direction)
                    time.sleep(1.0)
                    msg = pos2dist(m_RCX3.Robot[1].Position.Axis[1])
                    print(msg)
                else:
                    m_RCX3.Robot[1].Jog(axis, direction)
                t = time.time()
            

    m_RCX3.Stop()
    #m_RCX3.AlarmReset();
    m_RCX3.Disconnect();    

def pos2dist(pos):
    dist = 360.0-pos
    dist = int(dist/10)
    msg = "{:d} : {:.4f}".format(dist, pos)
    return msg

if __name__ == "__main__":
    main()
