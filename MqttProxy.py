import paho.mqtt.client as mqtt

from actors import *
from output_pins import *
from secret import *

commands = {
    0: {ACTION: ADD_DIRECTION, DIRECTION: FORWARD},
    1: {ACTION: ADD_DIRECTION, DIRECTION: LEFT},
    2: {ACTION: ADD_DIRECTION, DIRECTION: RIGHT},
    3: {ACTION: ADD_DIRECTION, DIRECTION: BACKWARD},
    4: {ACTION: OK},
    5: {ACTION: CANCEL}
}


class MqttProxy:

    def __init__(self, on_message_func):
        mqttc = mqtt.Client()
        mqttc.on_message = lambda client, obj, msg: on_message_func(int(msg.payload))

        mqttc.username_pw_set(MQTT_USER, MQTT_PASS)
        mqttc.connect(MQTT_HOST, MQTT_PORT)
        mqttc.subscribe(MQTT_TOPIC, 0)

        while True:
            mqttc.loop()
