import serial
import time
from serial.tools.list_ports import comports

class DramController:
    port = ""

    buttonRed = 0
    buttonBlue = 0
    buttonGreen = 0
    buttonOrange = 0

    buttonRedLed = 0
    buttonBlueLed = 0
    buttonGreenLed = 0
    buttonOrangeLed = 0

    IMU = (0,0,0)
    MIC = 0
    NunChuk = None

    def __init__(self):
        self.port = self.getPort("Arduino Zero")
        self.NunChuk = NunChuk()
        ser = serial.Serial(self.port, 9600, timeout = 0)
        if(ser.is_open):
            ser.close()
            ser.open()

    def getPort(self, name):
        portName = ''
        portList = list(comports())
        for port in portList:
            if port[1].startswith(name):
                portName = port[0]
        return(portName)



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