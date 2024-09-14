#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .BaseController import BaseController


class InputOutputController(BaseController):
    def __init__(self):
        self._input = []
        # @AssociationType fischertechnik.controller.Input[]
        # @AssociationMultiplicity *
        # @AssociationKind Aggregation
        self._counter = []
        # @AssociationType fischertechnik.controller.Counter[]
        # @AssociationMultiplicity *
        # @AssociationKind Aggregation
        self._output = []
        # @AssociationType fischertechnik.controller.Output[]
        # @AssociationMultiplicity *
        # @AssociationKind Aggregation
        self._motor = []
        # @AssociationType fischertechnik.controller.Motor[]
        # @AssociationMultiplicity *
        # @AssociationKind Aggregation
        self._servomotor = []
        # @AssociationType fischertechnik.controller.Servomotor[]
        # @AssociationMultiplicity *
        # @AssociationKind Aggregation
        self._i2c = []
        # @AssociationType fischertechnik.controller.I2C[]
        # @AssociationMultiplicity *
        # @AssociationKind Aggregation
        BaseController.__init__(self)

    def set_output(self, idx, output):
        """@ParamType idx int
        @ParamType output fischertechnik.controller.Output"""
        self._output[idx - 1] = output

    def get_output(self, idx):
        """@ParamType idx int"""
        return self._output[idx - 1]

    def set_motor(self, idx, motor):
        """@ParamType idx int()
        @ParamType motor fischertechnik.controller.Motor"""
        self._motor[idx - 1] = motor

    def get_motor(self, idx):
        """@ParamType idx int
        @ReturnType fischertechnik.controller.Motor"""
        return self._motor[idx - 1]

    def set_servomotor(self, idx, servomotor):
        """@ParamType idx int()
        @ParamType motor fischertechnik.controller.Servomotor"""
        self._servomotor[idx - 1] = servomotor

    def get_servomotor(self, idx):
        """@ParamType idx int
        @ReturnType fischertechnik.controller.Motor"""
        return self._servomotor[idx - 1]

    def set_input(self, idx, input):
        """@ParamType idx int
        @ParamType input fischertechnik.controller.Input"""
        self._input[idx - 1] = input

    def get_input(self, idx):
        """@ParamType idx int
        @ReturnType fischertechnik.controller.Input"""
        return self._input[idx - 1]

    def set_counter(self, idx, counter):
        """@ParamType idx int
        @ParamType counter fischertechnik.controller.Counter"""
        self._counter[idx - 1] = counter

    def get_counter(self, idx):
        """@ParamType idx int
        @ReturnType fischertechnik.controller.Counter"""
        return self._counter[idx - 1]

    def set_i2c(self, idx, i2c):
        """@ParamType idx int
        @ParamType i2c fischertechnik.controller.I2C"""
        self._i2c[idx - 1] = i2c

    def get_i2c(self, idx):
        """@ParamType idx int
        @ReturnType fischertechnik.controller.I2C"""
        return self._i2c[idx - 1]
