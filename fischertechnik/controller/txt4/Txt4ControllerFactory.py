#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from ft import fttxt2

from .Txt4Controller import Txt4Controller
from .Txt4ControllerInfo import Txt4ControllerInfo
from ..ControllerFactory import ControllerFactory


class Txt4ControllerFactory(ControllerFactory):

    __master = None

    def create_graphical_controller(self, ext = 0):
        """@ReturnType fischertechnik.controller.GraphicalInputOutputController"""
        if ext > 0 and self.__master is None:
            raise Exception('Creating extension without master')
        if ext == 0:
            self.__master = Txt4Controller(fttxt2())
            return self.__master

        controller_info_list = self.__master._txt.getControllerInfoList()
        lchar=repr(ext)
        for i in range(1, len(controller_info_list)):
            if controller_info_list[i].get_role().endswith(lchar):
                return self.create_graphical_controller_from_info(self.__master, controller_info_list[i])

        raise Exception('Extension for index %d does not exist' % ext)

    def create_graphical_controller_from_info(self, controller, info):
        """@ReturnType fischertechnik.controller.GraphicalInputOutputController"""
        return Txt4Controller(controller._txt.getController(info))

    def get_controller_info_list(self, controller):
        """@ReturnType A list of fischertechnik.controller.ControllerInfo"""
        txt = controller._txt
        list = []
        for i in range(txt.nslaves + 1):
            list.append(Txt4ControllerInfo(controller, i))
        return list


