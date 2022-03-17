import serial
import time
from serial.tools.list_ports import comports

class DramController:
    port = ""
    ser = None

    buttonRed = 0
    buttonBlue = 0
    buttonGreen = 0
    buttonOrange = 0

    buttonRedLed = 0
    buttonBlueLed = 0
    buttonGreenLed = 0
    buttonOrangeLed = 0

    leds = [0,0,0,0,0]

    seg1 = 0
    seg2 = 0

    vibrator = 0
    buzzer = 0

    IMU = (0,0,0)
    MIC = 0
    NunChuk = None

    def __init__(self):
        self.port = self.getPort("Arduino Zero")
        self.NunChuk = NunChuk()
        self.ser = serial.Serial(self.port, 9600, timeout = 0)
        if(self.ser.is_open):
            self.ser.close()
            self.ser.open()

    def getPort(self, name):
        portName = ''
        portList = list(comports())
        for port in portList:
            if port[1].startswith(name):
                portName = port[0]
        return(portName)

    def readButtons(self):
        return [self.buttonBlue, self.buttonGreen, self.ButtonRed, self.buttonOrange]


    def sendData(self):
        str = "{" + str(self.leds[0]) + str(self.leds[1]) + str(self.leds[2]) + str(self.leds[3]) + str(self.leds[4]) + str(self.buttonRedLed) + str(self.buttonGreenLed) + str(self.buttonOrangeLed) + str(self.buttonBlueLed) + str(self.seg1) + str(self.seg2) + str(self.vibrator) + str(self.buzzer) + "}"
        self.ser.write(str)


class NunChuk:
    joyX = 129
    joyY = 131
    buttonZ = 0
    buttonC = 0
    accel = (0,0,0)
    roll = 0
    pitch = 0

    def __init__(self):
        self.roll = 0