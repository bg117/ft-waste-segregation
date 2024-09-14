import socket
import ssl

import paho.mqtt.client as mqtt


class Client:

    KEEP_ALIVE = 30

    def __init__(self, client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp",
                 path="/"):
        self.handler = {}
        self.connected = False
        self.paho_client = mqtt.Client(client_id, clean_session, userdata, protocol, transport)
        if transport == 'websockets':
            self.paho_client.ws_set_options(path=path)
        self.paho_client.on_disconnect = self.__on_disconnect
        self.paho_client.on_connect = self.__on_connect
        self.paho_client.on_message = self.__on_message

    def __del__(self):
        self.disconnect()

    def connect(self, host, port, keepalive, bind_address, user, password):
        if 'beemo.eu' in host or 'fischertechnik-cloud.com' in host:
            try:
                context = ssl.create_default_context()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                context.wrap_socket(s, server_hostname="*.beemo.eu")
                self.paho_client.tls_set_context(context)
            except:
                pass
        if user and password:
            self.paho_client.username_pw_set(user, password)
        self.paho_client.connect(host, port, keepalive, bind_address)
        self.paho_client.loop_start()

    def disconnect(self):
        if self.paho_client:
            self.paho_client.disconnect()
            self.paho_client.loop_stop()

    def is_connected(self):
        return self.connected

    def subscribe(self, topic, callback, qos=0):
        self.handler[topic] = {"callback": callback, "qos": qos}
        if self.connected == True:
            self.paho_client.subscribe(topic, qos)

    def unsubscribe(self, topic):
        del self.handler[topic]
        if self.connected == True:
            self.paho_client.unsubscribe(topic)

    def publish(self, topic, payload=None, qos=0, retain=True):
        return self.paho_client.publish(topic, payload, qos, retain)

    def will_set(self, topic, payload=None, qos=0, retain=False):
        self.paho_client.will_set(topic, payload, qos, retain)

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            print("Unexpected connection.")
        else:
            for topic in self.handler.copy():
                self.paho_client.subscribe(topic, self.handler[topic]["qos"])
            self.connected = True

    def __on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")
        else:
            self.connected = False

    def __on_message(self, client, userdata, msg):
        for topic in self.handler.copy():
            if mqtt.topic_matches_sub(topic, msg.topic):
                self.handler[topic]["callback"](msg)
