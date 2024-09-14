#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4ColorSensor import Txt4ColorSensor
from .Txt4NTCResistor import Txt4NTCResistor
from .Txt4PhotoTransistor import Txt4PhotoTransistor
from .Txt4MiniSwitch import Txt4MiniSwitch
from .Txt4Resistor import Txt4Resistor
from .Txt4TrailFollower import Txt4TrailFollower
from .Txt4UltrasonicDistanceMeter import Txt4UltrasonicDistanceMeter
from ..InputFactory import InputFactory


class Txt4InputFactory(InputFactory):
    def create_ntc_resistor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.NTCResistor"""
        return Txt4NTCResistor(controller, identifier)

    def create_photo_resistor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Resistor"""
        return Txt4Resistor(controller, identifier)

    def create_ultrasonic_distance_meter(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.UltrasonicDistanceMeter"""
        return Txt4UltrasonicDistanceMeter(controller, identifier)

    def create_photo_transistor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.PhotoTransistor"""
        return Txt4PhotoTransistor(controller, identifier)

    def create_color_sensor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.ColorSensor"""
        return Txt4ColorSensor(controller, identifier)

    def create_trail_follower(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType TailFollower"""
        return Txt4TrailFollower(controller, identifier)

    def create_mini_switch(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.MiniSwitch"""
        return Txt4MiniSwitch(controller, identifier)
