class SensorHandler:
    """
    Class to contain sensor configuration,
    the condition on when to trigger an action
    and the action method itself
    """
    def __init__(self, sconfig, condition, callbacks=None, data_type='default'):
        """
        Parameters
        ----------
        sconfig : dict
        condition : func
        callbacks : [func]
            you can add multiple callbacks, they will be called in order
        data_type : str
            "gauge" or "counter"
        """
        self.condition = condition
        self.callbacks = callbacks

        # parse config
        self.sconfig = sconfig
        self.sensor_id = sconfig.get('id')
        if data_type == 'default':
            self.data_type = sconfig['data_type']
        else:
            self.data_type = data_type
        self.type = sconfig.get('type')
        self.subtype = sconfig.get('subtype')
        port = self.sconfig.get('port')
        if port:
            self.port = port[0]

    def eval_condition(self, timestamp, value, unit, **kwargs):
        """
        Function that will be called when a message arrives for this handler
        It evaluates the condition, and calls the callbacks

        Parameters
        ----------
        timestamp : int
        value : float
        unit : str
        kwargs : dict
        """
        kwargs.update({'sconfig': self.sconfig})  # put the config in the kwargs for the condition method
        try:
            if self.condition(timestamp=timestamp, value=value, unit=unit, **kwargs):
                self.do_callbacks(timestamp=timestamp, value=value, unit=unit, **kwargs)
        except Exception as e:
            print("Error evaluating condition! {}".format(str(e)))

    @property
    def topic(self):
        return "/sensor/{}/{}".format(self.sensor_id, self.data_type)

    def do_callbacks(self, timestamp, value, unit, **kwargs):
        """
        Call all methods in self.callbacks with all available arguments

        Parameters
        ----------
        timestamp : int
        value : float
        unit : str
        kwargs : dict
        """
        if self.callbacks:
            for callback in self.callbacks:
                try:
                    callback(timestamp=timestamp, value=value, unit=unit, **kwargs)
                except Exception as e:
                    print("Error during callback! {}".format(str(e)))
        else:
            self.default_callback()

    def default_callback(self):
        """
        If no callback is configured, just print something
        """
        print("The default callback method for {} has been triggered!".format(self.sensor_id))
