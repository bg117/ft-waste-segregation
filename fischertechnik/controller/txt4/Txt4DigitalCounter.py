from ..DigitalCounter import DigitalCounter


class Txt4DigitalCounter(DigitalCounter):

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.counter(identifier)
        controller._txt.update_config()
        DigitalCounter.__init__(self, controller, identifier)

    def get_state(self):
        return self.instance.state()

    def get_count(self):
        return self.instance.distance

    def reset(self):
        self.instance.reset()

    def is_open(self):
        return self.get_state() == 0

    def is_closed(self):
        return self.get_state() == 1

    def is_dark(self):
        return self.get_state() == 0

    def is_bright(self):
        return self.get_state() == 1