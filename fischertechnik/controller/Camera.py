#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .USB import USB

class Camera(USB):
    def __init__(self, controller, identifier):
        USB.__init__(self, controller, identifier)

    def start(self, width=320, height=240, fps=15, debug=False):
        pass

    def stop(self):
        pass

    def get_frame(self):
        """@ReturnType string"""
        pass

    def is_running(self):
        """@ReturnType boolean"""
        pass

