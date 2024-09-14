import paho.mqtt.client as mqtt

from ..mqtt.Client import Client


class MqttClient(Client):

    def __init__(self, client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp",
                 path="/"):
        Client.__init__(self, client_id, clean_session, userdata, protocol, transport, path)

    def __del__(self):
        Client.__del__(self)

    def connect(self, host, port, keepalive=Client.KEEP_ALIVE, bind_address="", user="", password=""):
        Client.connect(self, host, port, keepalive, bind_address, user, password)