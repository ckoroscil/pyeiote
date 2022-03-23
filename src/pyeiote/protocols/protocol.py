from .mdns import MDNS
from .ssdp import SSDP
from .nbdgm import NBDGM
from .sip import SIP

class Protocol(object):
    def __new__(cls, name, *args, **kwargs):

        if name.upper() == 'MDNS':
            return MDNS(*args, **kwargs)
        if name.upper() == 'SSDP':
            return SSDP(*args, **kwargs)
        if name.upper() == 'NBDGM':
            return NBDGM(*args, **kwargs)
        if name.upper() == 'SIP':
            return SIP(*args, **kwargs)

        raise Exception('Unknown protocol: {}'.format(name))