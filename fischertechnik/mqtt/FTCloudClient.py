from ..mqtt.Client import Client
from ..mqtt.Constants import MQTT_USER, MQTT_PASSWORD


class FTCloudClient(Client):

    HOST = "rabbitmq-data-live.beemo.eu"
    PORT = 443

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if FTCloudClient.__instance == None:
            FTCloudClient()
        return FTCloudClient.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if FTCloudClient.__instance != None:
            raise Exception("This class is a Singleton!")
        else:
            Client.__init__(self, transport="websockets", path="/ws")
            FTCloudClient.__instance = self

    def __del__(self):
        Client.__del__(self)

    def connect(self, host=HOST, port=PORT, keepalive=Client.KEEP_ALIVE, bind_address="", user=MQTT_USER, password=MQTT_PASSWORD):
        Client.connect(self, host, port, keepalive, bind_address, user, password)

    def publish(self, topic, payload=None, qos=2, retain=True):
        return Client.publish(self, topic, payload, qos, retain)
