#!/usr/bin/python
# -*- coding: UTF-8 -*-
import signal
import atexit
from .Txt4Loudspeaker import Txt4Loudspeaker
from ..GraphicalInputOutputController import GraphicalInputOutputController

class Txt4Controller(GraphicalInputOutputController):

    INPUTS = 8
    COUNTER = 4
    OUTPUT = 8
    MOTOR = 4
    SERVOMOTOR = 3
    I2C = 10
    USB = 2

    def __init__(self, txt):
        GraphicalInputOutputController.__init__(self)
        
        atexit.register(self.cleanup)

        self._input = [None] * self.INPUTS
        self._counter = [None] * self.COUNTER
        self._output = [None] * self.OUTPUT
        self._motor = [None] * self.MOTOR
        self._servomotor = [None] * self.SERVOMOTOR
        self._i2c = [None] * self.I2C
        self._usb = [None] * self.USB
        self._loudspeaker = Txt4Loudspeaker(self)
        self._txt = txt

    def cleanup(self, *args):

        for motor in self._motor:
            if motor is not None:
                motor.stop()

        for output in self._output:
            if output is not None:
                output.instance.setLevel(0)

        for counter in self._counter:
            if counter is not None:
                counter.reset()
