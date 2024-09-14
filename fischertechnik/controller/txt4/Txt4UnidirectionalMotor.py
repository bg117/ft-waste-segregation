#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..UnidirectionalMotor import UnidirectionalMotor


class Txt4UnidirectionalMotor(UnidirectionalMotor):
    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.output(identifier)
        controller._txt.update_config()
        UnidirectionalMotor.__init__(self, controller, identifier)

    def set_speed(self, speed):
        """Sets the Speed at which the engine should run.
        @ParamType speed int
        The speed range is between 0 (stop the motor) and 512
        (maximum speed)
        @ReturnType void"""
        self.validate_value(speed)
        self.instance.setLevel(speed)

    def get_speed(self):
        """Speed at which the engine is running. The speed range is between 0 (stop the motor) and 512 (maximum speed)
        @ReturnType int"""
        return self.instance.pwm

    def stop(self):
        """Sets the speed to zero and stops the motor."""
        self.instance.setLevel(0)

    def is_running(self):
        """Returns true if the distance has not yet been reached.
        @ReturnType bool"""
        return self.instance.pwm != 0
