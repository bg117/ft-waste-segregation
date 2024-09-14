from ..Compressor import Compressor


class Txt4Compressor(Compressor):

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.output(identifier)
        controller._txt.update_config()
        Compressor.__init__(self, controller, identifier)

    def on(self):
        """@ReturnType void"""
        self.instance.setLevel(512)

    def off(self):
        """@ReturnType void"""
        self.instance.setLevel(0)

    def is_on(self):
        """@ReturnType boolean"""
        return self.get_value() > 0

    def is_off(self):
        """@ReturnType boolean"""
        return self.get_value() == 0