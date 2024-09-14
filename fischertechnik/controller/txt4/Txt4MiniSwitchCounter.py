from .Txt4Counter import Txt4Counter
from .Txt4MiniSwitch import Txt4MiniSwitch

class Txt4MiniSwitchCounter(Txt4Counter, Txt4MiniSwitch):

    def __init__(self, controller, identifier):
         Txt4Counter.__init__(self, controller, identifier)
