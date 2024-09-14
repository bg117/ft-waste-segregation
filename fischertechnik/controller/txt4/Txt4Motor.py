#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Motor import Motor


class Txt4Motor(Motor):

    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.motor(identifier)
        controller._txt.update_config()
        Motor.__init__(self, controller, identifier)

    def set_speed(self, speed, direction = Motor.CCW):
        """Sets the Speed at which the engine should run.
        @ParamType speed int
        The speed range is between 0 (stop the motor) and 512
        (maximum speed)
        @ReturnType void"""
        self.validate_speed(speed)
        speed = speed * direction
        self.instance.speed_set(speed)

    def get_speed(self):
        """Speed at which the engine is running. The speed range is between 0 (stop the motor) and 512 (maximum speed)
        @ReturnType int"""
        return self.instance.pwm

    def is_running(self):
        """Returns true if the distance has not yet been reached.
        @ReturnType bool"""
        return self.instance.pwm != 0

    def start(self):
        """Starts the motor."""
        self.instance.start_speed(self.get_speed())

    def stop(self):
        """Sets the speed to zero and stops the motor."""
        self.instance.stop()

    def coast(self):
        """Sets the speed to zero and coasts the motor."""
        self.instance.coast()
