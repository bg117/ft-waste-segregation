#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Encodermotor import Encodermotor
from ..Motor import Motor


class Txt4Encodermotor(Encodermotor):

    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.encoder(identifier)
        controller._txt.update_config()
        Encodermotor.__init__(self, controller, identifier)

    def set_distance(self, distance, *sync_to):
        """Setting the engine speed, which is measured via the fast counters, which must be connected for this purpose.
        @ParamType distance int
        Indicates how many counts the motor should turn
        (The encoder motor requires 72 counters per axis rotation)
        @ParamType *sync_to fischertechnik.controller.Encodermotor
        This allows to synchronize motors. For example to realize a straight run. The motor object to be synchronized is transferred here."""
        self.validate_distance(distance)
        motors = []
        for i in sync_to:
            motors.append(i.instance)
        if distance == 0:
            self.stop_sync(*sync_to)
        else:
            self.instance.syncDistance(distance, *motors)

    def set_speed(self, speed, direction = Motor.CCW):
        """Sets the Speed at which the engine should run.
        @ParamType speed int
        The speed range is between 0 (stop the motor) and 512
        (maximum speed)
        @ReturnType void"""
        self.validate_speed(speed)
        speed = speed * direction
        self.instance.speed_set(speed)

    def get_distance(self):
        """@ReturnType int"""
        return self.instance.motor_distance

    def get_speed(self):
        """Speed at which the engine is running. The speed range is between 0 (stop the motor) and 512 (maximum speed)
        @ReturnType int"""
        return self.instance.pwm

    def is_running(self):
        """Returns true if the distance has not yet been reached.
        @ReturnType bool"""
        return self.instance.isrunning and self.instance.pwm != 0

    def start(self):
        """Starts the motor."""
        self.start_sync()

    def start_sync(self, *sync_to):
        """@ParamType *sync_to fischertechnik.controller.Encodermotor
        This allows to synchronize motors. For example to realize a straight run. The motor object to be synchronized is transferred here."""
        motors = []
        for i in sync_to:
            motors.append(i.instance)
        self.instance.syncStart(*motors)

    def stop_sync(self, *sync_to):
        """@ParamType *sync_to fischertechnik.controller.Encodermotor
        This allows to synchronize motors. For example to realize a straight run. The motor object to be synchronized is transferred here."""
        motors = []
        for i in sync_to:
            motors.append(i.instance)
        self.instance.syncStop(*motors)

    def stop(self):
        """Sets the speed to zero and stops the motor."""
        self.instance.stop()

    def coast(self):
        """Sets the speed to zero and coasts the motor."""
        self.instance.coast()
