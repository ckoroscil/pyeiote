from .base import BaseDevice
import random
import uuid

"""
default_protocol_config = {
    "protocol_config": [{
        "MDNS": {
            "frequency": 1
        }
    }]
}
"""

default_protocol_config = {
    "uuid": uuid.uuid1(),
    "protocol_config": [{
        "mdns": {
            "frequency": random.randint(30, 60),
            "type": "response",
            "an": [{
                "type": "PTR",
                "rname": '_http._tcp.local',
                "rdata": '{manufacturer} {model}._http._tcp.local',
                "rclass": 'IN',
                "ttl": 4500
            }],
            "ar": [
                {
                    "type": "A",
                    "rname": '{hostname}.local',
                    "rdata": '{ipv4}',
                    "rclass": 'IN',
                    "ttl": 120
                },
                {
                    "type": "SRV",
                    "rname": '{manufacturer} {model}._http._tcp.local',
                    "rclass": 'IN',
                    "port": 80,
                    "target": '{hostname}.local',
                    "ttl": 120
                },
                {
                    "type": "TXT",
                    "rname": '{manufacturer} {model}._http._tcp.local',
                    "rdata": None,
                    "rclass": 'IN',
                    "ttl": 4500
                }
            ],
        },
        "mdns": {
            "frequency": random.randint(30, 60),
            "type": "response",
            "an": [{
                "type": "PTR",
                "rname": '_ipp._tcp.local',
                "rdata": '{manufacturer} {model}._ipp._tcp.local',
                "rclass": 'IN',
                "ttl": 4500
            }],
            "ar": [
                {
                    "type": "A",
                    "rname": '{hostname}.local',
                    "rdata": '{ipv4}',
                    "rclass": 'IN',
                    "ttl": 120
                },
                {
                    "type": "SRV",
                    "rname": '{manufacturer} {model}._ipp._tcp.local',
                    "rclass": 'IN',
                    "port": 631,
                    "target": '{hostname}.local',
                    "ttl": 120
                },
                {
                    "type": "TXT",
                    "rname": '{manufacturer} {model}._ipp._tcp.local',
                    "rdata": [b'txtvers=1', 'ty={manufacturer} {model}', 'usb_MFG={manufacturer}', 
                        b'usb_MDL=XP-440 Series', 'product=({manufacturer} {model})', b'pdl=application/octet-stream,image/pwg-raster,image/urf,image/jpeg', b'rp=ipp/print', b'qtotal=1', 
                        b'Color=T', b'Duplex=F', b'Scan=T', b'Fax=F', b'kind=document,envelope,photo', b'PaperMax=legal-A4', b'URF=CP1,PQ4-5,OB9,OFU0,RS360,SRGB24,W8,IS1,V1.4,MT1-3-8-10-11-12', 
                        b'mopria-certified=1.3', b'priority=30', 'adminurl=http://{hostname}.local.:80/PRESENTATION/BONJOUR', b'note=', 'UUID={uuid}', b'TLS=1.2'],
                    "rclass": 'IN',
                    "ttl": 4500
                }
            ],
        },
        "nbdgm": {
            "frequency": 45,
            "type": "browser"
        }
    }]
}

"""
<DNSRR  rrname='EPSON XP-440 Series._ipp._tcp.local.' type=TXT rclass=32769 ttl=4500 rdlen=478 rdata=[b'txtvers=1', b'ty=EPSON XP-440 Series', b'usb_MFG=EPSON', 
b'usb_MDL=XP-440 Series', b'product=(EPSON XP-440 Series)', b'pdl=application/octet-stream,image/pwg-raster,image/urf,image/jpeg', b'rp=ipp/print', b'qtotal=1', 
b'Color=T', b'Duplex=F', b'Scan=T', b'Fax=F', b'kind=document,envelope,photo', b'PaperMax=legal-A4', b'URF=CP1,PQ4-5,OB9,OFU0,RS360,SRGB24,W8,IS1,V1.4,MT1-3-8-10-11-12', 
b'mopria-certified=1.3', b'priority=30', b'adminurl=http://EPSON773A62.local.:80/PRESENTATION/BONJOUR', b'note=', b'UUID=cfe92100-67c4-11d4-a45f-389d92773a62', b'TLS=1.2']
"""

class Printer(BaseDevice):
    def __init__(self, user_config):
        super(Printer, self).__init__(default_protocol_config, user_config)

