from .Output import Output


class UnidirectionalMotor(Output):

    def __init__(self, controller, identifier):
        """@ParamType controller fischertechnik.controller.BaseController
        @ParamType identifier int"""
        Output.__init__(self, controller, identifier)

    def set_speed(self, speed):
        """Sets the Speed at which the engine should run.
        @ParamType speed int
        The speed range is between 0 (stop the motor) and 512
        (maximum speed)
        @ReturnType void"""
        pass

    def get_speed(self):
        """Speed at which the engine is running. The speed range is between 0 (stop the motor) and 512 (maximum speed)
        @ReturnType int"""
        pass

    def stop(self):
        """Sets the speed to zero and stops the motor."""
        pass

    def is_running(self):
        """Returns true if the distance has not yet been reached.
        @ReturnType bool"""
        pass
