#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .Txt4Servomotor import Txt4Servomotor
from ..ServomotorFactory import ServomotorFactory


class Txt4ServomotorFactory(ServomotorFactory):

    def create_servomotor(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.GraphicalInputOutputController
        @ParamType identifier int
        @ReturnType fischertechnik.controller.Servomotor"""
        return Txt4Servomotor(controller, identifier)
