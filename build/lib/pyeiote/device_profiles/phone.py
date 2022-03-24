from .base import BaseDevice


default_protocol_config = {
    "protocol_config": [
        {
            "SIP": {
                "frequency": 300,
                "type": "register"
            }
        },
        {
            "SIP": {
                "frequency": 100,
                "type": "invite"
            }
        }
    ]
}

class Phone(BaseDevice):
    def __init__(self, user_config):
        super(Phone, self).__init__(default_protocol_config, user_config)

