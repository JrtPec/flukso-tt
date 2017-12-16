import paho.mqtt.client as mqtt


class Subscriber:
    def __init__(self, flm, handlers):
        """
        Parameters
        ----------
        flm : str
        handlers [SensorHandler]
        """
        self.flm = flm
        self.handlers = handlers

    def _on_message(self, client, userdata, msg):
        for handler in self.handlers:
            if mqtt.topic_matches_sub(handler.topic, msg.topic):
                timestamp, value, unit = self._decode_payload(msg.payload)
                handler.eval_condition(timestamp=timestamp, value=value, unit=unit)
                break  # only handle 1 handler per sensor for now TODO handle more

    @staticmethod
    def _decode_payload(payload):
        decoded = payload.decode('utf-8')
        timestamp, value, unit = decoded.strip('[]').split(', ')
        timestamp = int(timestamp)
        value = float(value)
        unit = unit.strip('"')
        return timestamp, value, unit

    def _on_connect(self, client, userdata, flags, rc):
        # print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        topics = [(handler.topic, 0) for handler in self.handlers]
        client.subscribe(topics)

    def run(self):
        """
        Connect to the FLM MQTT Broker and loop forever
        """
        client = mqtt.Client()
        client.on_message = self._on_message
        client.on_connect = self._on_connect
        client.connect(self.flm, 1883, 60)
        client.loop_forever()
