#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .IOUnit import IOUnit


class USB(IOUnit):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        IOUnit.__init__(self, controller, identifier)
        self._controller.set_usb(self._identifier, self)
