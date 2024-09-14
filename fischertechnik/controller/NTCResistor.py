#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Resistor import Resistor

class NTCResistor(Resistor):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        Resistor.__init__(self, controller, identifier)

    def get_temperature(self):
        """@ReturnType float"""
        pass

