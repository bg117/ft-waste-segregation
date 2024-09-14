from .Txt4Counter import Txt4Counter


class Txt4EncodermotorCounter(Txt4Counter):

    def __init__(self, controller, identifier):
        Txt4Counter.__init__(self, controller, identifier)
    
    def get_count(self):
        if self.motor is not None:
            return self.motor.instance.motor_distance
        return self.instance.distance

    def set_motor(self, motor):
        self.motor = motor
