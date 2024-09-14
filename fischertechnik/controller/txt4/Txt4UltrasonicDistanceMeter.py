#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..UltrasonicDistanceMeter import UltrasonicDistanceMeter


class Txt4UltrasonicDistanceMeter(UltrasonicDistanceMeter):

    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.ultrasonic(identifier)
        controller._txt.update_config()
        UltrasonicDistanceMeter.__init__(self, controller, identifier)

    def get_distance(self):
        """@ReturnType int"""
        return self.instance.distance
