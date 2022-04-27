from .printer import Printer
from .generic import Generic
from .phone import Phone
from .switch import Switch
from .streaming import Streaming
from .nas import NAS

class Device(object):
    def __new__(cls, cfg):
        device_type = cfg['type'].lower()

        if device_type == 'printer':
            return Printer(cfg)
        if device_type == 'generic':
            return Generic(cfg)
        if device_type == 'phone':
            return Phone(cfg)
        if device_type == 'switch':
            return Switch(cfg)
        if device_type == 'streaming':
            return Streaming(cfg)
        if device_type == 'nas':
            return NAS(cfg)

        raise Exception('Unknown device type: {}'.format(device_type))
