from zeroconf import ServiceBrowser, Zeroconf
from time import sleep

_flm = None


class _MyListener(object):
    def remove_service(self, zeroconf, type, name):
        pass
        # print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        global _flm
        info = zeroconf.get_service_info(type, name)
        # print("Service %s added, service info: %s" % (name, info))
        _flm = info.server


def discover_flm():
    """
    Scan your local network for the address of your FLM

    Returns
    -------
    str
    """
    zeroconf = Zeroconf()
    listener = _MyListener()
    browser = ServiceBrowser(zeroconf, "_mqtt._tcp.local.", listener)
    for _ in range(100):
        if _flm is None:
            sleep(1)
        else:
            zeroconf.close()
            return _flm
    else:
        raise LookupError("No FLM found in local network")
