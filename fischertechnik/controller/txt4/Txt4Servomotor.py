#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Servomotor import Servomotor


class Txt4Servomotor(Servomotor):

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.servo(identifier)
        controller._txt.update_config()
        Servomotor.__init__(self, controller, identifier)

    def set_position(self, position):
        """@ParamType position int"""
        self.validate_position(position)
        self.instance.pwm_set(position)

    def get_position(self):
        """Position of servo motor. The position range is between 0 and 512
        @ReturnType int"""
        return self.instance.pwm
