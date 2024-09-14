#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ..ControllerInfo import ControllerInfo

class Txt4ControllerInfo(ControllerInfo):
    def __init__(self, controller, num):
        txt = controller._txt
        ControllerInfo.__init__(self, txt.get_txt_name(num))
        self.uid = txt.get_txt_uid(num)
        self.sn = txt.get_txt_SN(num)
        self.index = num

