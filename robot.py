import clr
clr.AddReference('C:\\Program Files (x86)\\Yamaha Motor\\RCX3-SDK\\bin\\RCX3CLI.dll')

from RCX3DOTNET import CRCX3, EBaudRate, EDataBit, EParityBit, EStopBit, EFlowControl
import RCX3DOTNET, math, time

class Robot():
    def __init__(self):
        self.m_RCX3 = CRCX3.Create()
        self.cnt=1
        #self.init()

    def ProtocalInit(self, mode):
        if mode == 'Ethernet':
            self.m_RCX3.Host = "192.168.0.2"
            self.m_RCX3.Port = 23
        elif mode == 'RS232':
            self.m_RCX3.Host = "COM"
            self.m_RCX3.Port = 6
            self.m_RCX3.BaudRate = EBaudRate.BPS_19200
            self.m_RCX3.DataBit = EDataBit.BITS_8
            self.m_RCX3.ParityBit = EParityBit.ODD
            self.m_RCX3.StopBit = EStopBit.ONE_BIT
            self.m_RCX3.FlowControl = EFlowControl.XON_XOFF

    def init(self, b):
        self.ProtocalInit('Ethernet')

        if self.m_RCX3.Connect():
            print("RCX3 : Connected.")
            msg = self.m_RCX3.Controller[1].Version
            print("Controller Version : " + str(msg.Major) + "." + str(msg.Minor) + " rev." + str(msg.Revision))
            msg = self.m_RCX3.Controller[1].PLDVersion
            print("PLD Version : " + str(msg.Major) + "." + str(msg.Minor) + " rev." + str(msg.Revision))
            msg = self.m_RCX3.Controller[1].DriverVersion[1]
            print("Driver Version : " + str(msg.Major) + "." + str(msg.Minor) + " rev." + str(msg.Revision))
            self.m_RCX3.Power = b
            self.m_RCX3.Servo = b
            #self.m_RCX3.Robot[1].Brake = False
            self.m_RCX3.Robot[1].AutoSpeed = 50
            self.m_RCX3.Robot[1].Speed = 40
            self.m_RCX3.Robot[1].ManualSpeed = 20
            self.m_RCX3.Robot[1].InchingDistance = 10000
            self.active = False
            self.RobotEndFunction = RCX3DOTNET.MotionEndFunction(self.callbackMotionEnd)
            #self.moveDist(1)
            return True
        else:
            print("RCX3 : Failed to connect.")
            return False

    def Disconnect(self):
        self.m_RCX3.Stop()
        self.m_RCX3.Servo = False
        self.m_RCX3.Power = False
        self.m_RCX3.Disconnect();    

    def Servo(self, b):
        self.m_RCX3.Servo = b

    def pos2dist(self, pos):
        mm = 360.0-pos
        cm = mm/10.0
        i_cm = int(cm)
        if (cm-i_cm) > 0.5:
            dist = math.ceil(cm)
        else:
            dist = math.floor(cm)
        return int(dist), cm

    def getPos(self):
        return self.pos2dist(self.m_RCX3.Robot[1].Position.Axis[1])

    def moveDist(self, d):
        while True:
            curr, f = self.getPos()
            if d == curr:
                break
            elif curr < d:
                self.m_RCX3.Robot[1].Inching(2, RCX3DOTNET.EMoveDirection.MINUS)
                print('-')
            else:
                self.m_RCX3.Robot[1].Inching(2, RCX3DOTNET.EMoveDirection.PLUS)
                print('+')
            print("curr, f, d : {}, {:.4f}, {}".format(curr, f, d))
            time.sleep(1.0)
    def moveX(self, d):
        self.SetRobotMotionEnd()
        self.m_RCX3.Robot[1].Axis[1].Move(d)
        self.blockUntilFinish()
    def moveY(self, d):
        self.SetRobotMotionEnd()
        self.m_RCX3.Robot[1].Axis[2].Move(d)
        self.blockUntilFinish()
    def moveCartesian(self, x, y):
        self.moveX(x)
        self.moveY(y)
    def moveAlign(self, dist, angle):
        theta = angle / 180.0 * math.pi
        x = 450-(dist*math.cos(theta))
        y = 350-(dist*math.sin(theta))
        self.moveCartesian(x, y)
        return x, y

    def printProp(self):
        print("Power : {}".format(self.m_RCX3.Power))
        print("Servo : {}".format(self.m_RCX3.Servo))
        print("Brake : {}".format(self.m_RCX3.Robot[1].Brake))

    def callbackMotionEnd(self, res, user):
        print("RES : " + str(res))
        print("USER : " + str(user))
        self.active = False
        self.cnt = self.cnt+1
    
    def SetRobotMotionEnd(self):
        self.active = True
        self.m_RCX3.SetMotionEnd(self.RobotEndFunction, self.cnt)

    # Robot[1].Jog(1, 2, 3) = [ base[+Far:, -:Near], mid[+Front:, -:Back], tip[+Down, -Up]
    def Inching(self, cmd, mm=10, spd=20):
        self.m_RCX3.Robot[1].ManualSpeed = spd
        d = int(mm*1000)
        #print(str(type(d)) + " : " + str(d))
        self.m_RCX3.Robot[1].InchingDistance = d
        self.SetRobotMotionEnd()
        if cmd == 'NEAR':
            self.m_RCX3.Robot[1].Inching(1, RCX3DOTNET.EMoveDirection.MINUS)
        elif cmd == 'FAR':
            self.m_RCX3.Robot[1].Inching(1, RCX3DOTNET.EMoveDirection.PLUS)
        elif cmd == 'FRONT':
            self.m_RCX3.Robot[1].Inching(2, RCX3DOTNET.EMoveDirection.PLUS)
        elif cmd == 'BACK':
            self.m_RCX3.Robot[1].Inching(2, RCX3DOTNET.EMoveDirection.MINUS)
        elif cmd == 'UP':
            self.m_RCX3.Robot[1].Inching(3, RCX3DOTNET.EMoveDirection.MINUS)
        elif cmd == 'DOWN':
            self.m_RCX3.Robot[1].Inching(3, RCX3DOTNET.EMoveDirection.PLUS)
        else:
            return False
        self.blockUntilFinish()
        return True

    # Robot[1].Jog(1, 2, 3) = [ base[+Far:, -:Near], mid[+Front:, -:Back], tip[+Down, -Up]
    def Jog(self, cmd, spd=20):
        self.m_RCX3.Robot[1].ManualSpeed = spd
        self.SetRobotMotionEnd()
        if cmd == 'NEAR':
            self.m_RCX3.Robot[1].Jog(1, RCX3DOTNET.EMoveDirection.MINUS)
        elif cmd == 'FAR':
            self.m_RCX3.Robot[1].Jog(1, RCX3DOTNET.EMoveDirection.PLUS)
        elif cmd == 'FRONT':
            self.m_RCX3.Robot[1].Jog(2, RCX3DOTNET.EMoveDirection.PLUS)
        elif cmd == 'BACK':
            self.m_RCX3.Robot[1].Jog(2, RCX3DOTNET.EMoveDirection.MINUS)
        elif cmd == 'UP':
            self.m_RCX3.Robot[1].Jog(3, RCX3DOTNET.EMoveDirection.MINUS)
        elif cmd == 'DOWN':
            self.m_RCX3.Robot[1].Jog(3, RCX3DOTNET.EMoveDirection.PLUS)
        else:
            return False
        self.blockUntilFinish()
        return True

    def blockUntilFinish(self):
        while True:
            if self.active == False:
                break

    def Origin(self, jnt, spd=20):
        self.m_RCX3.Robot[1].ManualSpeed = spd
        self.SetRobotMotionEnd()
        self.m_RCX3.Robot[1].Axis[jnt].Origin()
        self.blockUntilFinish()
