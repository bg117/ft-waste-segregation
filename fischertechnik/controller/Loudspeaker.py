#!/usr/bin/python
# -*- coding: UTF-8 -*-
from .IOUnit import IOUnit


class Loudspeaker(IOUnit):
    def __init__(self, controller):
        IOUnit.__init__(self, controller, 0)
        self._controller.set_loudspeaker(self)


    def play(self, soundId, repeat, path):
        """@ParamType soundId int
        @ParamType repeat int"""
        pass

    def is_playing(self):
        pass

    def set_volume(self, volume):
        """@ParamType volume int"""
        pass

    def get_volume(self):
        """@ReturnType int"""
        pass

    def stop(self):
        pass

