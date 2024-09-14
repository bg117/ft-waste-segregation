#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..LightSource import LightSource


class Txt4LightSource(LightSource):
    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.output(identifier)
        controller._txt.update_config()
        LightSource.__init__(self, controller, identifier)

    def set_brightness(self, brightness):
        """@ParamType brightness int"""
        self.validate_value(brightness)
        self.instance.setLevel(brightness)

    def get_brightness(self):
        """@ReturnType int"""
        return self.instance.pwm

    def is_on(self):
        """@ReturnType boolean"""
        return self.get_brightness() > 0

    def is_off(self):
        """@ReturnType boolean"""
        return self.get_brightness() == 0
