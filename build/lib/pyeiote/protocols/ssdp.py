# SSDP
# https://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol

from lib2to3.pytree import Base
from statistics import mode
from .base import BaseProtocol
from scapy.all import Ether, IP, UDP, RandShort
from . import const

"""
srcip
srcmac
"""

class SSDP(BaseProtocol):
    def __init__(self, *args, **cfg):
        self.frequency = 7200
        self.count = 3
        self.delay = 3
        super(SSDP, self).__init__(*args, **cfg)

    def generate_packet(self):
        srcip = self.device.get('ipv4', None)
        srcmac = self.device.get('mac', None)

        dstip = const.IPV4_MULTICAST_SSDP
        dstmac = const.ETH_BROADCAST
        dport = const.UDP_SSDP
        ssdp_type = self.config.get('type', 'discover')

        payload = self.__generate_payload(ssdp_type, dstip, dport)
        
        return Ether(src=srcmac, dst=dstmac)/IP(src=srcip, dst=dstip, ttl=255)/UDP(sport=RandShort(), dport=dport)/payload
    
    def __generate_payload(self, ssdp_type, server, port):
        if ssdp_type.lower() == "discover":
            return "M-SEARCH * HTTP/1.1\r\n" \
                "HOST: " + server + ":" + str(port) + "" \
                "MAN: \"ssdp:discover\"\r\n" \
                "MX: 3\r\n" \
                "ST: ssdp:all\r\n\r\n"
        elif ssdp_type.lower() == "upnp":
            return "M-SEARCH * HTTP/1.1\r\n" \
                "HOST: " + server + ":" + str(port) + "" \
                "MAN: \"ssdp:discover\"\r\n" \
                "MX: 3\r\n" \
                "ST: upnp:rootdevice\r\n\r\n"
        else:
            raise Exception('Unknown SSDP type: {}'.format(ssdp_type))
