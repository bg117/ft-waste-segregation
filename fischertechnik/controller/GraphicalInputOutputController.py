#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .InputOutputController import InputOutputController

class GraphicalInputOutputController(InputOutputController):
    def __init__(self):
        self._ir = None
        # @AssociationType fischertechnik.controller.IR
        # @AssociationMultiplicity 1
        self._gui = None
        # @AssociationType fischertechnik.controller.Window
        # @AssociationMultiplicity 1
        self._usb = []
        # @AssociationType fischertechnik.controller.USB[]
        # @AssociationMultiplicity *
        self._loudspeaker = None
        # @AssociationType fischertechnik.controller.Loudspeaker
        # @AssociationMultiplicity 1
        self._mic = None
        # @AssociationType fischertechnik.controller.Microphone
        # @AssociationMultiplicity 1
        InputOutputController.__init__(self)

    def set_window(self, window):
        """@ParamType window fischertechnik.controller.Window"""
        pass

    def exec_controller(self):
        pass

    def set_usb(self, idx, usb):
        """@ParamType idx int
        @ParamType usb fischertechnik.controller.USB"""
        self._usb[idx - 1] = usb

    def get_usb(self, idx):
        """@ParamType idx int"""
        return self._usb[idx - 1]

    def set_loudspeaker(self, loudspeaker):
        """@ReturnType fischertechnik.controller.Loudspeaker"""
        self._loudspeaker = loudspeaker

    def get_loudspeaker(self):
        """@ReturnType fischertechnik.controller.Loudspeaker"""
        return  self._loudspeaker

    def get_microphone(self):
        """@ReturnType fischertechnik.controller.Microphone"""
        pass

    def get_ir(self):
        """@ReturnType fischertechnik.controller.IR"""
        pass

