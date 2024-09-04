from typing import Callable
import ftrobopy


def pwm(status):
    return 512 if status else 0


BIO = 0
NP = 1
REC = 2
PLASTIC = 3

# setup the TXT controller 4.0
# unless indicated otherwise, all inputs and outputs are connected to the master controller (txt1)


class UltrasonicArray:
    def __init__(self, txt: ftrobopy.ftrobopy):
        self._array = [None, None, None]

        self.front = txt.ultrasonic(1)  # I1
        self.object_confirm = txt.ultrasonic(2)  # I2
        self[BIO] = txt.ultrasonic(3)  # I3
        self[NP] = txt.ultrasonic(4)  # I4
        self[REC] = txt.ultrasonic(5)  # I5
        self[PLASTIC] = txt.ultrasonic(6) # I6

    def __getitem__(self, key):
        return self._array[key]

    def __setitem__(self, key, value):
        self._array[key] = value


class EncoderArray:
    def __init__(self, txt: ftrobopy.ftrobopy):
        self.preface = txt.motor(1)  # M1, preface motor
        self.main = txt.motor(2)  # M2, main motor


class Solenoid:
    def __init__(self, master: ftrobopy.ftrobopy, slave: ftrobopy.ftrobopy, index):
        self._input = master.output(index)  # O1, O2, O3
        self._output = slave.output(index)

    def open(self):
        self._input.setLevel(pwm(True))  # pwm full power
        self._output.setLevel(pwm(False))

    def close(self):
        self._input.setLevel(pwm(False))
        self._output.setLevel(pwm(True))

class Camera:
    def __init__(self, txt: ftrobopy.ftrobopy):
        self._txt = txt

    def start(self):
        return self._txt.startCameraOnline(640, 480)

    def stop(self):
        return self._txt.stopCameraOnline()

    def frame(self):
        return self._txt.getCameraFrame()


class TXTController:
    def __init__(self):
        self._txt1 = ftrobopy.ftrobopy(host="auto")
        self._txt2 = ftrobopy.ftrobopy(
            host="auto", use_extension=True
        )  # slave controller

        # print out firmware versions
        print("TXT (master) firmware version: ", self._txt1.getFirmwareVersion())
        print("TXT (slave) firmware version: ", self._txt2.getFirmwareVersion())

        self.ultrasonic = UltrasonicArray(self._txt1)
        self.solenoid = [
            Solenoid(self._txt1, self._txt2, 1),
            Solenoid(self._txt1, self._txt2, 2),
            Solenoid(self._txt1, self._txt2, 3),
        ]
        self.encoder = EncoderArray(self._txt1)

        self.camera = Camera(self._txt1)

        self.weight_sensor = self._txt1.input(7)  # I7
        self.compressor = self._txt1.output(4)  # O4

    def start(self):
        self._txt1.startOnline()
        self._txt2.startOnline()

    def stop(self):
        self._txt1.stopOnline()
        self._txt2.stopOnline()

    def run(self, process: Callable):
        self.start()
        process(self)
        self.stop()
