#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4CombinedSensor import Txt4CombinedSensor
from .Txt4CombinedSensor6Pin import Txt4CombinedSensor6Pin
from .Txt4EnvironmentSensor import Txt4EnvironmentSensor
from .Txt4GestureSensor import Txt4GestureSensor
from ..I2CFactory import I2CFactory


class Txt4I2CFactory(I2CFactory):
    def create_environment_sensor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.EnvironmentSensor"""
        return Txt4EnvironmentSensor(controller, identifier)

    def create_combined_sensor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.CombinedSensor"""
        return Txt4CombinedSensor(controller, identifier)

    def create_combined_sensor_6pin(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.CombinedSensor"""
        return Txt4CombinedSensor6Pin(controller, identifier)

    def create_gesture_sensor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.GestureSensor"""
        return Txt4GestureSensor(controller, identifier)
