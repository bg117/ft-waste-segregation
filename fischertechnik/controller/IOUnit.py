#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..events.EventLoop import EventLoop

class IOUnit(object):

    _event_loop = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self._controller = controller
        """@AttributeType fischertechnik.controller.BaseController"""
        self._identifier = identifier
        """@AttributeType int"""
        self._event_loop = EventLoop.getInstance()
        """@AttributeType fischertechnik.events.EventLoop"""
    
    def add_change_listener(self, property_name, callback):
        """@ParamType property_name string
        @ParamType callback Any"""
        self._event_loop.add_change_listener(self, property_name, callback)
        
    def remove_change_listener(self, property_name, callback):
        """@ParamType property_name string
        @ParamType callback Any"""
        self._event_loop.remove_change_listener(self, property_name, callback)
