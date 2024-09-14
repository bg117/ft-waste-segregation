#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..MagneticValve import MagneticValve

class Txt4MagneticValve(MagneticValve):

    state = 0
    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.output(identifier)
        controller._txt.update_config()
        MagneticValve.__init__(self, controller, identifier)

    def on(self):
        self.instance.setLevel(512)

    def off(self):
        self.instance.setLevel(0)

    def is_on(self):
        """@ReturnType boolean"""
        return self.instance.pwm != 0

    def is_off(self):
        """@ReturnType boolean"""
        return self.instance.pwm == 0
