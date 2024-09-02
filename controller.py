import ftrobopy

# setup the TXT controller 4.0

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

class TXTController:
    def __init__(self):
        self.txt = ftrobopy.ftrobopy(host='auto')

        self.ultrasonic = UltrasonicArray(self.txt)
        self.solenoid_input_valves = SolenoidInputValveArray(self.txt)

        self.encoders = EncoderArray
        self.weight_sensor = self.txt.input(5) # I5
        self.compressor = self.txt.output(1) # O1