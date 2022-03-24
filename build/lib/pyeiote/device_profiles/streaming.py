from .base import BaseDevice
import uuid
import random

default_protocol_config = {
    "protocol_config": [{
        "MDNS": {
            "frequency": 1
        }
    }]
}

roku_protocol_config = {
    "mac": "b0:ee:7b",
    "uuid": str(uuid.uuid1()),
    "protocol_config": [{
        "mdns": {
            "frequency": random.randint(30, 60),
            "type": "response",
            "an": [{
                "type": "PTR",
                "rname": '_spotify-connect._tcp.local',
                "rdata": '{uuid}._spotify-connect._tcp.local',
                "rclass": 'IN',
                "ttl": 4500
            }],
            "ar": [
                {
                    "type": "TXT",
                    "rname": '{uuid}._spotify-connect._tcp.local',
                    "rdata": 'CPath=/zc',
                    "rclass": 'IN',
                    "ttl": 4500
                },
                {
                    "type": "SRV",
                    "rname": '{uuid}._spotify-connect._tcp.local',
                    "rclass": 'IN',
                    "port": random.randint(64000, 65000),
                    "target": '{hostname}.local',
                    "ttl": 120
                },
                {
                    "type": "A",
                    "rname": '{hostname}.local',
                    "rdata": '{ipv4}',
                    "rclass": 'IN',
                    "ttl": 120
                },
                {
                    "type": "NSEC",
                    "rname": '{uuid}._spotify-connect._tcp.local',
                    "next": '{uuid}._spotify-connect._tcp.local',
                    "rclass": 'IN',
                    "bitmap": [16, 33],
                    "ttl": 4500
                },
                {
                    "type": "NSEC",
                    "rname": '{hostname}.local',
                    "next": '{hostname}.local',
                    "rclass": 'IN',
                    "bitmap": [1],
                    "ttl": 120
                }
            ],
        }
    }]
}

class Streaming(BaseDevice):
    def __init__(self, user_config):
        default_config = default_protocol_config

        manufacturer = user_config.get('manufacturer', None)

        if manufacturer.lower() == 'roku':
            default_config = roku_protocol_config
        
        super(Streaming, self).__init__(default_config, user_config)
        
        

