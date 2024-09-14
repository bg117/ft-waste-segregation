#!/usr/bin/python
# -*- coding: UTF-8 -*-

class MotorFactory(object):
    def __init__(self):
        object.__init__(self)

    def create_motor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Motor"""
        pass

    def create_encodermotor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Encodermotor"""
        pass



