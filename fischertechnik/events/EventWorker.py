import threading

from .Event import Event


class EventWorker(object):

    def __init__(self, target, property_name, callback):
        """@ParamType target fischertechnik.controller.IOUnit
        @ParamType property string"""
        self.__target = target
        self.__property_name = property_name
        self.__callback = callback
        self.__prev_value = self.__get_value()

    @property
    def callback(self):
        return self.__callback

    @property
    def target(self):
        return self.__target

    @property
    def property_name(self):
        return self.__property_name

    def run(self):
        current_value = self.__get_value()
        if current_value != self.__prev_value:
            self.__prev_value = current_value
            self.__callback(Event(self.__property_name, self.__target))

    def __get_value(self):

        get_value = getattr(self.__target, self.__property_name, None)
        if get_value is not None:
            return get_value

        get_value = getattr(self.__target, 'get_' + self.__property_name, None)
        if get_value is not None:
            return get_value()

        get_value = getattr(self.__target, 'is_' + self.__property_name, None)
        if get_value is not None:
            return get_value()

        return None