#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4Encodermotor import Txt4Encodermotor
from .Txt4Motor import Txt4Motor
from ..MotorFactory import MotorFactory


class Txt4MotorFactory(MotorFactory):

    def create_motor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Motor"""
        return Txt4Motor(controller, identifier)

    def create_encodermotor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Encodermotor"""
        return Txt4Encodermotor(controller, identifier)
