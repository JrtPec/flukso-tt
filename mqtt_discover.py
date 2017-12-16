import paho.mqtt.client as mqtt
import json

sensor_config_topic = "/device/+/config/sensor"

_config = None


def _on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))
    client.subscribe(sensor_config_topic)


def _on_message(client, userdata, msg):
    # The callback for when a PUBLISH message is received from the server.
    global _config
    if mqtt.topic_matches_sub(sensor_config_topic, msg.topic):
        _config = msg.payload


def discover_config(flm):
    """
    Listen to your FLM to fetch all sensor configurations

    Parameters
    ----------
    flm : str

    Returns
    -------
    dict
    """
    client = mqtt.Client()
    client.on_connect = _on_connect
    client.on_message = _on_message

    client.connect(flm, 1883, 60)
    for _ in range(100):
        if _config is None:
            client.loop()
        else:
            client.disconnect()
            return json.loads(_config.decode('utf-8'))
    else:
        client.disconnect()
        raise LookupError('No config received')