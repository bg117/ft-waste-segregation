#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..NTCResistor import NTCResistor

class Txt4NTCResistor(NTCResistor):

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.resistor(identifier)
        controller._txt.update_config()
        NTCResistor.__init__(self, controller, identifier)

    def get_resistance(self):
        """@ReturnType int"""
        return self.instance.resistance

    def get_temperature(self):
        """@ReturnType float"""
        return self.instance.ntcTemperature()
