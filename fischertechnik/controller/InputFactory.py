#!/usr/bin/python
# -*- coding: UTF-8 -*-

class InputFactory(object):
    def __init__(self):
        object.__init__(self)

    def create_ntc_resistor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.NTCResistor"""
        pass

    def create_photo_resistor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Resistor"""
        pass

    def create_ultrasonic_distance_meter(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.UltrasonicDistanceMeter"""
        pass

    def create_photo_transistor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.PhotoTransistor"""
        pass

    def create_color_sensor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.ColorSensor"""
        pass

    def create_trail_follower(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.TrailFollower"""
        pass

    def create_mini_switch(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.MiniSwitch"""
        pass

