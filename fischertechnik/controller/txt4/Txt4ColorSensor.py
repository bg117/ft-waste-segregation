#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..ColorSensor import ColorSensor

class Txt4ColorSensor(ColorSensor):

    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.colorsensor(identifier)
        controller._txt.update_config()
        ColorSensor.__init__(self, controller, identifier)

    def get_voltage(self):
        """@ReturnType int"""
        return self.instance.voltage
