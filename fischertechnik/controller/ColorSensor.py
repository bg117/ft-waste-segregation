#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Voltmeter import Voltmeter

class ColorSensor(Voltmeter):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        Voltmeter.__init__(self, controller, identifier)

    def get_voltage(self):
        """@ReturnType int"""
        pass

