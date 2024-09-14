#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4Compressor import Txt4Compressor
from .Txt4LightSource import Txt4LightSource
from .Txt4MagneticValve import Txt4MagneticValve
from .Txt4UnidirectionalMotor import Txt4UnidirectionalMotor
from ..OutputFactory import OutputFactory


class Txt4OutputFactory(OutputFactory):

    def create_lamp(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.LightSource"""
        return Txt4LightSource(controller, identifier)

    def create_led(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.LightSource"""
        return Txt4LightSource(controller, identifier)

    def create_magnetic_valve(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.MagneticValve"""
        return Txt4MagneticValve(controller, identifier)

    def create_compressor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Motor"""
        return Txt4Compressor(controller, identifier)

    def create_unidirectional_motor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.UnidirectionalMotor"""
        return Txt4UnidirectionalMotor(controller, identifier)