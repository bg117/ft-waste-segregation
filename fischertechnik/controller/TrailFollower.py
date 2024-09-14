#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Input import Input

class TrailFollower(Input):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        Input.__init__(self, controller, identifier)

    def get_state(self):
        """@ReturnType int"""
        pass

