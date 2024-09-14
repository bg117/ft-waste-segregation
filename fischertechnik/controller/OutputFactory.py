#!/usr/bin/python
# -*- coding: UTF-8 -*-

class OutputFactory(object):
    def __init__(self):
        object.__init__(self)

    def create_lamp(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.LightSource"""
        pass

    def create_led(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.LightSource"""
        pass

    def create_magnetic_valve(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.MagneticValve"""
        pass

    def create_compressor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Compressor"""
        pass

    def create_unidirectional_motor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.UnidirectionalMotor"""
        pass