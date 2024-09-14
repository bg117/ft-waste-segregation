#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .I2C import I2C

class GestureSensor(I2C):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        I2C.__init__(self, controller, identifier)

    def enable_light(self):
        pass

    def get_ambient(self):
        pass

    def get_color(self):
        pass

    def enable_gesture(self, threshold = 50):
        pass

    def get_gesture(self):
        pass

    def enable_proximity(self, threshold = 50):
        pass

    def get_proximity(self):
        pass
