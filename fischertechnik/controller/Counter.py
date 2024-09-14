#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .IOUnit import IOUnit

class Counter(IOUnit):
    """Abstract base class for counter."""
    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        IOUnit.__init__(self, controller, identifier)
        self._controller.set_counter(self._identifier, self)

    def get_state(self):
        pass

    def get_count(self):
        pass

    def reset(self):
        pass

