#!/usr/bin/python
# -*- coding: UTF-8 -*-

class I2CFactory(object):
    def __init__(self):
        object.__init__(self)

    def create_combined_sensor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.CombinedSensor"""
        pass

    def create_combined_sensor_6pin(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.CombinedSensor"""
        pass

    def create_environment_sensor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.EnvironmentSensor"""
        pass

    def create_gesture_sensor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.GestureSensor"""
        pass
