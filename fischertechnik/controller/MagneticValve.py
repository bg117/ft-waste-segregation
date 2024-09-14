#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Output import Output

class MagneticValve(Output):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        Output.__init__(self, controller, identifier)

    def on(self):
        """@ReturnType void"""
        pass

    def off(self):
        """@ReturnType void"""
        pass

    def is_on(self):
        """@ReturnType boolean"""
        pass

    def is_off(self):
        """@ReturnType boolean"""
        pass

