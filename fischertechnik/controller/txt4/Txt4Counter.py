from ..Counter import Counter


class Txt4Counter(Counter):

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        self.instance = controller._txt.counter(identifier)
        controller._txt.update_config()
        Counter.__init__(self, controller, identifier)

    def get_state(self):
        return self.instance.state()

    def get_count(self):
        return self.instance.distance

    def reset(self):
        self.instance.reset()
