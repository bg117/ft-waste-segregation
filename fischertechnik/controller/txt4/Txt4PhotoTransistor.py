#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4Controller import Txt4Controller
from ..PhotoTransistor import PhotoTransistor

class Txt4PhotoTransistor(PhotoTransistor):

    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.switch(identifier)
        controller._txt.update_config()
        PhotoTransistor.__init__(self, controller, identifier)
    
    def get_state(self):
        """@ReturnType int"""
        return self.instance.state()

    def is_dark(self):
        """@ReturnType boolean"""
        return self.get_state() == 0

    def is_bright(self):
        """@ReturnType boolean"""
        return self.get_state() == 1