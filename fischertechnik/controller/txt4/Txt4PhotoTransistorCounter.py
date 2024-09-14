from .Txt4Counter import Txt4Counter
from .Txt4PhotoTransistor import Txt4PhotoTransistor

class Txt4PhotoTransistorCounter(Txt4Counter, Txt4PhotoTransistor):

    def __init__(self, controller, identifier):
         Txt4Counter.__init__(self, controller, identifier)