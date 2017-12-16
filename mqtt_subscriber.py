import paho.mqtt.client as mqtt


class Subscriber:
    def __init__(self, flm, handlers=None):
        """
        Parameters
        ----------
        flm : str
        handlers : [SensorHandler]
        """
        self.flm = flm
        if handlers is None:
            self.handlers = []
        else:
            self.handlers = handlers

    def _on_connect(self, client, userdata, flags, rc):
        # print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        # subscribe to topics
        topics = {handler.topic for handler in self.handlers}  # use a set to avoid duplicate topics
        topics = [(topic, 0) for topic in topics]
        client.subscribe(topics)

        # add callbacks
        for handler in self.handlers:
            client.message_callback_add(handler.topic, handler._on_message)

    def run(self):
        """
        Connect to the FLM MQTT Broker and loop forever
        """
        client = mqtt.Client()
        client.on_connect = self._on_connect
        client.connect(self.flm, 1883, 60)
        client.loop_forever()
