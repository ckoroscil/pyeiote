from .base import BaseDevice
import random


default_protocol_config = {
    "protocol_config": [{
        "nbns": {
            "frequency": random.randint(30, 60)
        },
        "nbdgm": {
            "frequency": random.randint(30, 60),
            "type": "browser",
            "cmd": "announcement",
            "server_types": [
                "workstation",
                "server",
                "print",
                "xenix",
                "nt_workstation",
                "dfs"
            ]
        },
        "nbdgm": {
            "frequency": random.randint(30, 60),
            "type": "browser",
            "cmd": "election"
        }
    }]
}
"""
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
"""

class NAS(BaseDevice):
    def __init__(self, user_config):
        super(NAS, self).__init__(default_protocol_config, user_config)

