#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4Counter import Txt4Counter
from .Txt4MiniSwitchCounter import Txt4MiniSwitchCounter
from .Txt4EncodermotorCounter import Txt4EncodermotorCounter
from .Txt4PhotoTransistorCounter import Txt4PhotoTransistorCounter
from ..CounterFactory import CounterFactory


class Txt4CounterFactory(CounterFactory):

    def create_counter(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Txt4Counter"""
        return Txt4Counter(controller, identifier)

    def create_mini_switch_counter(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.xt4MiniSwitchCounter"""
        return Txt4MiniSwitchCounter(controller, identifier)

    def create_photo_transistor_counter(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Txt4PhotoTransistorCounter"""
        return Txt4PhotoTransistorCounter(controller, identifier)

    def create_encodermotor_counter(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Txt4EncodermotorCounter"""
        return Txt4EncodermotorCounter(controller, identifier)