from .base import BaseProtocol
from scapy.all import Packet, Ether, IP, UDP, DNS, DNSRR, DNSRRSRV, DNSRRNSEC, dns_compress
from . import const
import uuid
import random

"""
device: manufacture
device: model
srcip
srcmac
"""

class MDNS(BaseProtocol):
    def __init__(self, *args, **cfg):
        self.frequency = 3600
        self.count = 1
        self.delay = 0
        super(MDNS, self).__init__(*args, **cfg)

    def generate_packet(self):
        srcip = self.device.get('ipv4', None)
        srcmac = self.device.get('mac', None)
        hostname = self.device.get('hostname', None)

        dstip = const.IPV4_MULTICAST_MDNS
        dstmac = self.__generate_dstmac(dstip)
        dport = const.UDP_MDNS
        sport = const.UDP_MDNS
        
        dns = self.__generate_dns()

        return Ether(src=srcmac, dst=dstmac)/IP(src=srcip, dst=dstip, ttl=255)/UDP(sport=sport, dport=dport)/dns_compress(dns)
    
    def __generate_dstmac(self, dstip):
        """
        An IP host group address is mapped to an Ethernet multicast address
        by placing the low-order 23-bits of the IP address into the low-order
        23 bits of the Ethernet multicast address 01-00-5E-00-00-00 (hex).
        https://datatracker.ietf.org/doc/html/rfc1112
        """
        octets = [ int(octet) for octet in dstip.split('.')[1:]]
        octets[0] = octets[0] & 0b1111111
        return '01:00:5e:{:02x}:{:02x}:{:02x}'.format(*octets)
    
    def __generate_dns(self):
        dns_type = self.config.get('type', "response")
        an = self.__generate_record(self.config.get('an', []))
        ar = self.__generate_record(self.config.get('ar', []))

        if dns_type == "response":
            return DNS(an=an, ar=ar, qd=None, rd=0, qr=1)
        else:
            return None

    def __generate_record(self, params):
        params = list(params)
        if len(params) > 1:
            return self.__generate_record(params[0:1])/self.__generate_record(params[1:])
        elif len(params) == 1:
            params = params[0]
            if params['type'] in ['PTR', 'TXT', 'A']:
                return DNSRR(rrname=params['rname'], type=params['type'], rclass=params['rclass'], ttl=params['ttl'], rdlen=None, rdata=params['rdata'])
            elif params['type'] in ['SRV']:
                return DNSRRSRV(rrname=params['rname'], type=params['type'], rclass=params['rclass'], ttl=params['ttl'], rdlen=None, priority=0, weight=0, port=params['port'], target=params['target'])
            elif params['type'] in ['NSEC']:
                return DNSRRNSEC(rrname=params['rname'], type=params['type'], rclass=params['rclass'], ttl=params['ttl'], nextname=params['next'], typebitmaps=params['bitmap'])
            else:
                raise Exception('unknown DNS type: {}'.format(params['type']))
        else:
            return None
