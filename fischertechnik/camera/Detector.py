class Detector(object):

    _identifier = 'identifier'

    def __init__(self, identifier):
        self._identifier = identifier
        self._callbacks = []

    def analyze_frame(self, frame):
        pass

    def detected(self):
        pass

    def draw_contour(self, frame):
        pass

    def set_identifier(self, identifier):
        self._identifier = identifier

    def get_identifier(self):
        return self._identifier

    def get_result(self):
        pass

    def add_change_listener(self, callback):
        if callback in self._callbacks:
            return
        self._callbacks.append(callback)

    def remove_change_listener(self, callback):
        if callback not in self._callbacks:
            return
        self._callbacks.remove(callback)

    # TODO: can be removed in the next release    
    def add_detection_listener(self, callback):
        if callback in self._callbacks:
            return
        self._callbacks.append(callback)

    # TODO: can be removed in the next release  
    def remove_detection_listener(self, callback):
        if callback not in self._callbacks:
            return
        self._callbacks.remove(callback)