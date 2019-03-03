from MqttProxy import MqttProxy


def on_message(client, obj, msg):
    print(str(msg.payload))


if __name__ == '__main__':
    client = MqttProxy(on_message)
