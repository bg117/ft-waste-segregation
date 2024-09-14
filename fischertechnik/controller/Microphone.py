#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .USB import USB


class Microphone(USB):
    def __init__(self, controller, identifier):
        USB.__init__(self, controller, identifier)

    def start(self):
        pass

    def stop(self):
        pass

    def get_volume(self):
        """@ReturnType float"""
        pass