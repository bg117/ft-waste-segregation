import json

class DetectorResult(object):
        
    def __init__(self, identifier, detected = False, value = None):
        self.identifier = identifier
        self.detected = detected
        self.value = value

    def to_string(self):
        return json.dumps(self, default=self.json_encode)

    def to_dict(self):
        return json.loads(self.to_string())

    def json_encode(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        else:
            return o.__dict__
