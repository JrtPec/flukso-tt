class SensorHandler:
    """
    Class to contain sensor configuration,
    the condition on when to trigger an action
    and the action method itself
    """
    def __init__(self, sconfig, data_type='default', timeout=1):
        """
        Parameters
        ----------
        sconfig : dict
            you can add multiple callbacks, they will be called in order
        data_type : str
            "gauge" or "counter"
        timeout : int | float
            timeout between callbacks in seconds
        """
        # parse config
        self.sconfig = sconfig
        self.sensor_id = sconfig.get('id')
        if data_type == 'default':
            self.data_type = sconfig['data_type']
        else:
            self.data_type = data_type

        self.timeout = timeout
        self._next_msg_time = 0

        self.on_message = None

    @property
    def topic(self):
        return "/sensor/{}/{}".format(self.sensor_id, self.data_type)

    def _on_message(self, client, userdata, msg):
        if self.on_message is None:
            raise NotImplementedError("No handler function set")

        timestamp, value, unit = self._decode_payload(msg.payload)
        if timestamp < self._next_msg_time:
            return
        done = self.on_message(timestamp=timestamp, value=value, unit=unit, sconfig=self.sconfig)

        if done and self.timeout > 1:
            self._next_msg_time = timestamp + self.timeout

    @staticmethod
    def _decode_payload(payload):
        decoded = payload.decode('utf-8')
        timestamp, value, unit = decoded.strip('[]').split(', ')
        timestamp = int(timestamp)
        value = float(value)
        unit = unit.strip('"')
        return timestamp, value, unit