# sip
# 

from random import randint
from .base import BaseProtocol
from scapy.all import Ether, IP, UDP
from . import const


"""
srcip
srcmac
"""

class SIP(BaseProtocol):
    def __init__(self, *args, **cfg):
        self.frequency = 60
        self.count = 1
        self.delay = 0
        super(SIP, self).__init__(*args, **cfg)

    def generate_packet(self):
        srcip = self.device.get('ipv4', None)
        srcmac = self.device.get('mac', None)

        dstip = self.config.get('dstip', '1.2.3.4')
        dstmac = self.config.get('dstmac', '01:02:03:04:05:06')
        sport = const.UDP_SIP
        dport = const.UDP_SIP
        sip_type = self.config.get('type', 'register')

        sip_options = {
            "server": self.config.get('server', 'sip.server.local'),
            "client": self.config.get('client', srcip),
            "callid": str(randint(10000,99999)),
            "user": self.config.get('user', '9195551212'),
            "useragent": self.device.get('user-agent', 'Generic UA')
        }
        
        payload = self.__generate_payload(sip_type, **sip_options)
        
        return Ether(src=srcmac, dst=dstmac)/\
            IP(src=srcip, dst=dstip)/\
            UDP(sport=sport, dport=dport)/\
            payload
    
    def __generate_payload(self, sip_type, **options):
        payload = ''
        
        if sip_type.lower() == 'register':
            payload = ("REGISTER sip:{server} SIP/2.0\r\n"
                "To: <sip:{user}@{server}:5060>\r\n"
                "Via: SIP/2.0/UDP {client}:30000;branch=z9hG4bKdeadb33f\r\n"
                "From: hacker <sip:{user}@{client}:30000>\r\n"
                "Call-ID: f9844fbe7dec140ca36500a0c91{callid}@{client}\r\n"
                "CSeq: 1 INVITE\r\n"
                "User-agent: {useragent}\r\n"
                "Max-Forwards: 5\r\n"
                "Content-Length: 0\r\n\r\n")
        elif sip_type.lower() == 'ok':
            payload = ("SIP/2.0 200 OK\r\n" + \
                "Via: SIP/2.0/UDP {client}:30000;branch=z9hG4bKdeadb33f\r\n" + \
                "To: <sip:{user}@{server}:5060>\r\n" + \
                "From: <sip:666@{client}:30000>\r\n" + \
                "Call-ID: f9844fbe7dec140ca36500a0c91{callid}@{client}\r\n" + \
                "CSeq: 1 INVITE\r\n" + \
                "Contact: <sip:{user}@{client}:5060>\r\n" + \
                "User-agent: {useragent}\r\n" + \
                "Max-Forwards: 5\r\n" + \
                "Content-Length: 0\r\n\r\n")
        elif sip_type.lower() == 'invite':
            payload = ("INVITE sip:{user}@{server} SIP/2.0\r\n" + \
                "To: \"test\"""<sip:{user}@{server}:5060>\r\n" + \
                "Via: SIP/2.0/UDP {client}:30000\r\n" + \
                "From: \"hacker\"""<sip:666@{client}:30000>\r\n" + \
                "Call-ID: f9844fbe7dec140ca36500a0c91{callid}@{client}\r\n" + \
                "CSeq: 1 INVITE\r\n" + \
                "Contact: <sip:{user}@{client}:5060>\r\n" + \
                "User-agent: {useragent}\r\n" + \
                "Max-Forwards: 0\r\n" + \
                "Content-Length: 0\r\n\r\n")

        return payload.format(**options)