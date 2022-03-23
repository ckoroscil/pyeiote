import random
import re
from .profiles import get_profiles
import logging
import string

logger = logging.getLogger('eiot-traffic-gen')
profiles = get_profiles()

def generate_hostname(name, manufacturer, mac):
    mac = ''.join(mac.split(':')[3:])

    if name:
        return name
    elif manufacturer and mac:
        return '{}{}'.format(manufacturer, mac)
    else:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

def generate_mac(device_type, mac):
    # user provided full mac
    if mac and re.match(r'^([0-9a-fA-F]{2}:){5}([0-9a-fA-F]{2})$', mac, re.IGNORECASE):
        return mac
    # user provided just OUI 
    elif mac and re.match(r'^([0-9a-fA-F]{2}:){2}([0-9a-fA-F]{2})$', mac, re.IGNORECASE):
        args = [mac] + [random.randint(0, 255) for i in range(3)]
        return "{}:{:02x}:{:02x}:{:02x}".format(*args)
    # Get a realistic OUI based on device type
    elif device_type in profiles.keys():
        vendor, config = random.choice(list(profiles[device_type].items()))
        args = [config['mac']] + [random.randint(0, 255) for i in range(3)]
        return "{}:{:02x}:{:02x}:{:02x}".format(*args)
    # generate random mac   
    else:
        args = [random.randint(0, 255) for i in range(6)]
        return ':'.join("{:02x}".format(octet) for octet in args)

def get_device_profile(device_type, manufacturer=None):
    available_profiles = profiles[device_type]
    if manufacturer and manufacturer.lower() in available_profiles.keys():
        return available_profiles[manufacturer.lower()]
    else:
        profile = random.choice(list(available_profiles.values())) if len(available_profiles.values()) > 0 else None
        profile = make_random_selections(profile)
        return profile if profile else {}

def make_random_selections(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = make_random_selections(value)
        return obj
    elif isinstance(obj, list):
        return random.choice(obj)
    else:
        return obj

def print_device(device):
    output = """
    type: {type}
    name: {name}
    manufacturer: {manufacturer}
    model: {model}
    mac: {mac}
    protocol_config: {protocol_config}
    """.format(**device)
    logger.info(output)