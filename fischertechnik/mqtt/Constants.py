import configparser

def read_out(a, b):
    configParser = configparser.RawConfigParser()
    configFilePath = r'/opt/ft/config/Fischertechnik/TXT_4.0_Menu.conf'
    configParser.read(configFilePath)
    value = configParser.get(a, b)
    return value

MQTT_USER = read_out('FischertechnikCloud', 'ft_mqtt_user')
MQTT_PASSWORD = read_out('FischertechnikCloud', 'ft_mqtt_password')
CONTROLLER_ID = read_out('FischertechnikCloud', 'ft_controller_id')
