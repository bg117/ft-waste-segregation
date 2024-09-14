#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..Resistor import Resistor

class Txt4Resistor(Resistor):

    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.resistor(identifier)
        controller._txt.update_config()
        Resistor.__init__(self, controller, identifier)

    def get_resistance(self):
        """@ReturnType int"""
        return self.instance.resistance
