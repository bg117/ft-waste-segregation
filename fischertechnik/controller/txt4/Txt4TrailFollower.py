#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ..TrailFollower import TrailFollower


class Txt4TrailFollower(TrailFollower):
    instance = None

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.trail_follower(identifier)
        controller._txt.update_config()
        TrailFollower.__init__(self, controller, identifier)

    def get_state(self):
        """@ReturnType int"""
        return self.instance.state()
