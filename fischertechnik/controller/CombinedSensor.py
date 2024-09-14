#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .I2C import I2C

class CombinedSensor(I2C):
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        I2C.__init__(self, controller, identifier)

    def get_acceleration_x(self):
        """@ReturnType float"""
        pass

    def get_acceleration_y(self):
        """@ReturnType float"""
        pass

    def get_acceleration_z(self):
        """@ReturnType float"""
        pass

    def get_rotation_x(self):
        """@ReturnType float"""
        pass

    def get_rotation_y(self):
        """@ReturnType float"""
        pass

    def get_rotation_z(self):
        """@ReturnType float"""
        pass

    def get_magnetic_field_x(self):
        """@ReturnType float"""
        pass

    def get_magnetic_field_y(self):
        """@ReturnType float"""
        pass

    def get_magnetic_field_z(self):
        """@ReturnType float"""
        pass

