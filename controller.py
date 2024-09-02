import ftrobopy

# setup the TXT controller 4.0
# unless indicated otherwise, all inputs and outputs are connected to the master controller (txt1)

class UltrasonicArray:
    def __init__(self, txt):
        self.front = txt.ultrasonic(1) # I1
        self.bio = txt.ultrasonic(2) # I2
        self.np_ultrasonic = txt.ultrasonic(3) # I3
        self.rec_ultrasonic = txt.ultrasonic(4) # I4

class EncoderArray:
    def __init__(self, txt):
        self.preface_enc = txt.motor(1) # M1, preface motor
        self.main_enc = txt.motor(2) # M2, main motor

class SolenoidInputValveArray:
    def __init__(self, txt):
        self.bio_input_valve = txt.output(2) # O2
        self.np_input_valve = txt.output(3) # O3
        self.rec_input_valve = txt.output(4) # O4

# slave controller
class SolenoidOutputValveArray:
    def __init__(self, txt):
        self.bio_output_valve = txt.output(1) # O1
        self.np_output_valve = txt.output(2) # O2
        self.rec_output_valve = txt.output(3) # O3

class TXTController:
    def __init__(self):
        self.txt1 = ftrobopy.ftrobopy(host='auto')
        self.txt2 = ftrobopy.ftrobopy(host='auto', use_extension=True) # slave controller

        # print out firmware versions
        print("TXT (master) firmware version: ", self.txt1.getFirmwareVersion())
        print("TXT (slave) firmware version: ", self.txt2.getFirmwareVersion())

        self.ultrasonic = UltrasonicArray(self.txt1)
        self.solenoid_input_valves = SolenoidInputValveArray(self.txt1)
        self.solenoid_output_valves = SolenoidOutputValveArray(self.txt2)
        self.encoders = EncoderArray(self.txt1)

        self.weight_sensor = self.txt1.input(5) # I5
        self.compressor = self.txt1.output(1) # O1