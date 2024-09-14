#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ControllerFactory(object):
    """Abstract factory to be inherited by a concrete factory per controller.
    E.g. TxtAbstractFactory"""
    def __init__(self):
        object.__init__(self)

    def create_graphical_controller(self, ext=0):
        """@ReturnType fischertechnik.controller.GraphicalInputOutputController"""
        pass

    def create_graphical_controller_from_info(self, controller, info):
        """@ReturnType fischertechnik.controller.GraphicalInputOutputController"""
        pass

    def get_controller_info_list(self, controller):
        """@return: A list of ControllerInfo"""
        pass

