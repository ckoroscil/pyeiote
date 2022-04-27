# NetBIOS Datagram Service (nbdgm)
# https://www.wireshark.org/docs/dfref/n/nbdgm.html

from .base import BaseProtocol
from scapy.all import Ether, IP, UDP, NBTDatagram, SMBMailSlot, SMB_Header, SMBNetlogon_Protocol_Response_Header
from . import const
from pyeiote.utils import network_to_broadcat

"""
srcip
srcmac
"""

class NBDGM(BaseProtocol):
    def __init__(self, *args, **cfg):
        self.frequency = 732
        self.count = 1
        self.delay = 0
        super(NBDGM, self).__init__(*args, **cfg)

    def generate_packet(self):
        srcip = self.device.get('ipv4', None)
        srcmac = self.device.get('mac', None)

        dstip = network_to_broadcat(self.device.get('network', None))
        dstmac = const.ETH_BROADCAST
        sport = const.UDP_NBDS
        dport = const.UDP_NBDS
        nbds_type = self.config.get('type', 'browser')
        hostname = self.device.get('name', None)
        mailslot_name = '\MAILSLOT\BROWSE'
        payload = self.__generate_payload(nbds_type, hostname)

        """
        <Ether  dst=ff:ff:ff:ff:ff:ff src=38:9d:92:77:3a:62 type=IPv4 |
        <IP  version=4 ihl=5 tos=0x0 len=229 id=0 flags=DF frag=0 ttl=64 proto=udp chksum=0xa994 src=192.168.7.36 dst=192.168.7.255 |
        <UDP  sport=netbios_dgm dport=netbios_dgm len=209 chksum=0x1ade |
        <NBTDatagram  Type=17 Flags=2 ID=125 SourceIP=192.168.7.36 SourcePort=138 Length=187 Offset=0 SourceName='EPSON773A62    ' SUFFIX1=file server service NULL1=0 DestinationName='WORKGROUP      ' SUFFIX2=16974 NULL2=0 |
        <Raw  load='\\xffSMB%\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x00\x00!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00!\x00V\x00\x03\x00\x01\x00\x00\x00\x02\x002\x00\\MAILSLOT\\BROWSE\x00\x01\x00\\x80\\xfc\n\x00EPSON773A62\x00\x00\x00\x00\x00\x06\x02\x02\x00\x00\x00\x00\x04U\\xaa\x00' |>>>>>
        """
        
        return Ether(src=srcmac, dst=dstmac)/\
            IP(src=srcip, dst=dstip, ttl=255)/UDP(sport=sport, dport=dport)/self.__generate_nbdgm(srcip, hostname, payload, mailslot_name)
    
    def __generate_nbdgm(self, srcip, hostname, payload, mailslot_name):
        cmd = self.config.get('cmd', 'election')

        if cmd == 'election':
            return NBTDatagram(Type=17, Flags=0x0a, SourceIP=srcip, SourcePort=const.UDP_NBDS, SourceName=str.encode(hostname), DestinationName=b'WORKGROUP')/\
                SMB_Header(Command=0x25, Flags=0x0, PIDLow=0)/\
                SMBNetlogon_Protocol_Response_Header(TotalDataCount=len(payload), TimeOut1=0, TimeOut2=0, DataCount=len(payload), DataOffset=86)/\
                SMBMailSlot(priority=0, name=mailslot_name, size=(len(mailslot_name) + len(payload) + 1))/self.__generate_election_request()
        elif cmd == 'announcement':
            #return NBTDatagram()/SMB()/SMBMailSlot()/self.__generate_host_announcement()
            return NBTDatagram()/SMB_Header(Flags=0)/SMBNetlogon_Protocol_Response_Header(TotalDataCount=33, TimeOut1=0, TimeOut2=0, DataCount=33, DataOffset=86)/SMBMailSlot(name=mailslot_name, size=50)/b'\x01\x01\x80\xfc\x0a\x00' + '{:\x00<16}'.format(hostname).encode() + b'\x04\x09\x03\x1a\x80\x00\x0f\x01\x55\xaa\x00'
        else:
            raise Exception('Unknown browser protocol command: {}'.format(cmd))

    def __generate_host_announcement(self):
        server_types = self.config.get('server_types', [])
    
    def __generate_election_request(self):
        pass

    def __generate_payload(self, nbds_type, hostname):
        payload = ''
        
        # hostname must be 16 bytes exactly. truncate longer, or pad shorter
        hostname = hostname[:16]
        hostname = hostname.encode('utf-8') + (b"\x00" * (16 - len(hostname)))

        if nbds_type.lower() == 'browser':
            payload = b"\x01\x00\x80\xfc\x0a\x00" + hostname + b"\x06\x02\x02\x00\x00\x00\x00\x04\x55\xaa\x00"
        
        return payload

        NBTDatagram(Type=17, Flags=2, SourceIP=srcip, SourcePort=dport, SourceName=str.encode(hostname), DestinationName=b'WORKGROUP', SUFFIX1='file server service', SUFFIX2=16974)/\
            SMB_Header(Command=0x25, Flags=0x0, PIDLow=0)/\
            SMBNetlogon_Protocol_Response_Header(TotalDataCount=len(payload), TimeOut1=0, TimeOut2=0, DataCount=len(payload), DataOffset=86)/\
            SMBMailSlot(priority=0, name=mailslot_name, size=(len(mailslot_name) + len(payload) + 1))/\
            payload