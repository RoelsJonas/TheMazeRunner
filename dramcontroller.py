import serial
import time

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
    MIC =
    NunChuk = None

    def __init__(self):
        self.port = getPort("Arduino Zero")
        self.NunChuk = NunChuk()


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