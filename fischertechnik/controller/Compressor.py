#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .Output import Output


class Compressor(Output):

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        Output.__init__(self, controller, identifier)

    def on(self):
        """@ParamType brightness int
        @ReturnType void"""
        pass

    def off(self):
        """@ReturnType int"""
        pass

    def is_on(self):
        """@ReturnType boolean"""
        pass

    def is_off(self):
        """@ReturnType boolean"""
        pass


