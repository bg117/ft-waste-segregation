#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .I2C import I2C

class EnvironmentSensor(I2C):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        I2C.__init__(self, controller, identifier)

    def needs_calibration(self):
        """@ReturnType boolean"""
        pass

    def get_accuracy(self):
        """@ReturnType int"""
        pass

    def get_temperature(self):
        """@ReturnType float"""
        pass

    def get_humidity(self):
        """@ReturnType float"""
        pass

    def get_pressure(self):
        """@ReturnType float"""
        pass

    def calibrate(self):
        """@ReturnType void"""
        pass

    def is_ready(self):
        """@ReturnType boolean"""
        pass

    def get_indoor_air_quality_as_text(self):
        """@ReturnType string"""
        pass

    def get_indoor_air_quality_as_number(self):
        """@ReturnType float"""
        pass

