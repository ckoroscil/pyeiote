from .base import BaseDevice

class Generic(BaseDevice):
    def __init__(self, user_config):
        super(Generic, self).__init__({}, user_config)

