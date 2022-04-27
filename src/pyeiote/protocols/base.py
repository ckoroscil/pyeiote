import threading
import random
from scapy.all import sendp
import logging
import os


logger = logging.getLogger('eiot-traffic-gen')

class BaseProtocol(threading.Thread):
    def __init__(self, stopFlag, device, **protocol_config):
        threading.Thread.__init__(self)
        self.stopFlag = stopFlag
        self.device = device
        self.config = protocol_config
        # populate '{VAR}' variables within protocol_config
        self.config = self.__resolve_vars(self.config, **self.device)

        self.frequency = self.config.get('frequency', self.frequency)
        self.count = self.config.get('count', self.count)
        self.delay = self.config.get('delay', self.delay)
        self.packet = self.generate_packet()

    def generate_packet(self):
        raise NotImplementedError
    
    def stop(self):
        self.stopFlag.set()

    def run(self):
        # Wait a random number of seconds for some randomization
        while not self.stopFlag.wait(random.randint(0, 60)):
            break
        
        while not self.stopFlag.wait(self.frequency):
            count = 1
            while not self.stopFlag.wait(self.delay):
                if count > self.count: break
                self.send_packet()
                count += 1

    def send_packet(self):
        sendp(self.packet, iface=os.environ["SCAPYIFACE"])
    
    def __resolve_vars(self, obj, **vars):
        if isinstance(obj, str):
            return obj.format(**vars)
        elif isinstance(obj, list):
            return [self.__resolve_vars(item, **vars) for item in obj]
        elif isinstance(obj, dict):
            ret = {}
            for k, v in obj.items():
                ret[self.__resolve_vars(k)] = self.__resolve_vars(v, **vars)
            return ret
        else:
            return obj

    