#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4Camera import Txt4Camera
from .Txt4Microphone import Txt4Microphone
from ..USBFactory import USBFactory


class Txt4USBFactory(USBFactory):

    def create_camera(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Camera"""
        return Txt4Camera(controller, identifier)

    def create_microphone(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Microphone"""
        return Txt4Microphone(controller, identifier)
