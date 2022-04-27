import threading
from .utils import generate_mac, generate_hostname
from ...protocols.protocol import Protocol
import logging

logger = logging.getLogger('eiot-traffic-gen')


class BaseDevice(threading.Thread):
    def __init__(self, default_config, user_config):
        threading.Thread.__init__(self)
        self.stopFlag = threading.Event()
        
        # merge the default config and user config
        self.cfg = default_config
        self.cfg.update(user_config)

        # Validate or generate a device mac address
        device_type = self.cfg.get('type', 'generic')
        self.cfg['mac'] = generate_mac(device_type, self.cfg.get('mac', None))

        # Validate or create a device hostname
        manufacturer = self.cfg.get('manufacturer', None)
        self.cfg['hostname'] = generate_hostname(self.cfg.get('name', None), manufacturer, self.cfg['mac'])
        
        self.protocols = self.__configure_protocols()
        self.threads = []
    
    def stop(self):
        self.stopFlag.set()

    def run(self):
        for protocol in self.protocols:
            protocol.start()
            self.threads.append(protocol)
    
    def __configure_protocols(self):
        ret = []
        protocol_config = self.cfg.get('protocol_config')
        logger.debug('configure protocol:{}'.format(protocol_config))

        for protocol in protocol_config:
            for name, protocol_options in protocol.items():
                ret.append(Protocol(name, self.stopFlag, self.cfg, **protocol_options))
        return ret
    