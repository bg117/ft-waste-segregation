#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Input import Input

class UltrasonicDistanceMeter(Input):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        Input.__init__(self, controller, identifier)

    def get_distance(self):
        """@ReturnType int"""
        pass

