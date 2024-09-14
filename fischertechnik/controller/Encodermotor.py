#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Motor import Motor


class Encodermotor(Motor):

    MIN_DISTANCE = 0
    MAX_DISTANCE = 65536

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        Motor.__init__(self, controller, identifier)

    def set_distance(self, distance, *sync_to):
        """@ParamType distance int
        @ParamType *sync_to fischertechnik.controller.Encodermotor"""
        pass

    def get_distance(self):
        """@ReturnType int"""
        pass

    def start_sync(self, *sync_to):
        """@ParamType *sync_to fischertechnik.controller.Encodermotor
        This allows to synchronize motors. For example to realize a straight run. The motor object to be synchronized is transferred here."""
        pass

    def stop_sync(self, *sync_to):
        """@ParamType *sync_to fischertechnik.controller.Motor
        This allows to synchronize motors. For example to realize a straight run. The motor object to be synchronized is transferred here."""
        pass

    def validate_distance(self, distance):
        if distance < self.MIN_DISTANCE or distance > self.MAX_DISTANCE:
            raise ValueError("Distance must be >={} and <={}".format(self.MIN_DISTANCE, self.MAX_DISTANCE))
