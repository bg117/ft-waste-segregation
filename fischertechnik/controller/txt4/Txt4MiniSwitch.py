#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4Controller import Txt4Controller
from ..MiniSwitch import MiniSwitch


class Txt4MiniSwitch(MiniSwitch):

    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.switch(identifier)
        controller._txt.update_config()
        MiniSwitch.__init__(self, controller, identifier)

    def get_state(self):
        """@ReturnType int"""
        return self.instance.state()

    def is_open(self):
        """@ReturnType boolean"""
        return self.get_state() == 0

    def is_closed(self):
        """@ReturnType boolean"""
        return self.get_state() == 1
