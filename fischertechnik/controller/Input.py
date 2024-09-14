#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .IOUnit import IOUnit

class Input(IOUnit):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        IOUnit.__init__(self, controller, identifier)
        self._controller.set_input(self._identifier, self)

    def get_state(self):
        pass
