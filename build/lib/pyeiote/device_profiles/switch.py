from .base import BaseDevice


default_protocol_config = {
    "protocol_config": [{
        "SSDP": {
            "frequency": 1
        }
    }]
}

class Switch(BaseDevice):
    def __init__(self, user_config):
        super(Switch, self).__init__(default_protocol_config, user_config)

