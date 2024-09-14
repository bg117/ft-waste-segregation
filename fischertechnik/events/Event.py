class Event(object):

    def __init__(self, property_name, target):
        """@ParamType property_name string
        @ParamType target object"""
        self._type = property_name
        self._target = target

    @property
    def type(self):
        return self._type

    @property
    def target(self):
        return self._target