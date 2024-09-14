#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .IOUnit import IOUnit

class Motor(IOUnit):

    # CCW = positive values, direction of rotation is left (0 to +512)
    # CW = negative values, direction of rotation is right (0 to -512)
    # These value ranges correspond to the old ROBOPro.
    CCW = 1
    CW = -1
    MIN_SPEED = -512
    MAX_SPEED = 512

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        IOUnit.__init__(self, controller, identifier)
        self._controller.set_motor(self._identifier, self)

    def set_speed(self, speed, direction):
        """Sets the Speed at which the engine should run.
        @ParamType speed int
        @ParamType direction int
        The speed range is between 0 (stop the motor) and 512
        (maximum speed)
        @ReturnType void"""
        pass

    def get_speed(self):
        """Speed at which the engine is running. The speed range is between 0 (stop the motor) and 512 (maximum speed)
        @ReturnType int"""
        pass

    def is_running(self):
        """Returns true if the distance has not yet been reached.
        @ReturnType bool"""
        pass

    def start(self):
        """Starts the motor."""
        pass

    def stop(self):
        """Sets the speed to zero and stops the motor."""
        pass

    def coast(self):
        """Sets the speed to zero and coasts the motor."""
        pass

    def validate_speed(self, speed):
        if speed < self.MIN_SPEED or speed > self.MAX_SPEED:
            raise ValueError("Speed must be >=-512 and <=512")