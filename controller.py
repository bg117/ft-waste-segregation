import ftrobopy

def pwm(status):
    return 512 if status else 0

# setup the TXT controller 4.0
# unless indicated otherwise, all inputs and outputs are connected to the master controller (txt1)

class UltrasonicArray:
    def __init__(self, txt):
        self.front = txt.ultrasonic(1) # I1
        self.bio = txt.ultrasonic(2) # I2
        self.np = txt.ultrasonic(3) # I3
        self.rec = txt.ultrasonic(4) # I4

class EncoderArray:
    def __init__(self, txt):
        self.preface = txt.motor(1) # M1, preface motor
        self.main = txt.motor(2) # M2, main motor

class Solenoid:
    def __init__(self, master, slave, index):
        self._input = master.input(index) # I1, I2, I3
        self._output = slave.output(index)

    def open(self):
        self._input.setLevel(pwm(True)) # pwm full power
        self._output.setLevel(pwm(False))

    def close(self):
        self._input.setLevel(pwm(False))
        self._output.setLevel(pwm(True))

# slave controller
class SolenoidArray:
    def __init__(self, master, slave):
        self.bio = Solenoid(master, slave, 1)
        self.nc = Solenoid(master, slave, 2)
        self.rec = Solenoid(master, slave, 3)

class TXTController:
    def __init__(self):
        self.txt1 = ftrobopy.ftrobopy(host='auto')
        self.txt2 = ftrobopy.ftrobopy(host='auto', use_extension=True) # slave controller

        # print out firmware versions
        print("TXT (master) firmware version: ", self.txt1.getFirmwareVersion())
        print("TXT (slave) firmware version: ", self.txt2.getFirmwareVersion())

        self.ultrasonic = UltrasonicArray(self.txt1)
        self.solenoid = SolenoidArray(self.txt1, self.txt2)
        self.encoder = EncoderArray(self.txt1)

        self.weight_sensor = self.txt1.input(5) # I5
        self.compressor = self.txt1.output(4) # O4