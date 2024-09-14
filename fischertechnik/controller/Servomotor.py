#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .IOUnit import IOUnit

class Servomotor(IOUnit):

    MIN_POSITION = 0
    MAX_POSITION = 512

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        IOUnit.__init__(self, controller, identifier)
        self._controller.set_servomotor(self._identifier, self)

    def set_position(self, position):
        """@ParamType position int"""
        pass

    def get_position(self):
        """Position of servo motor. The position range is between 0 and 512
        @ReturnType int"""
        pass

    def validate_position(self, position):
        if position < self.MIN_POSITION or position > self.MAX_POSITION:
            raise ValueError("Position must be >0 and <=512")

