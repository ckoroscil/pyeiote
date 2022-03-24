import yaml
import re
import random
import logging
import uuid


logger = logging.getLogger('eiot-traffic-gen')

def load_yaml(config):
    ret = ''
    with open(config, "r") as stream:
        try:
            ret = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)
    return ret

def generate_network(network):
    if network and re.match(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:/\d{1,2}?)$', network):
        return network
    else:
        subnet = random.choice(['10.0.0.0', '192.168.0', '172.16.0.0'])
        return '{}/24'.format(subnet)

"""
Get the next available ip address within a subnet
"""
def get_ip_address(cidr, requested_ip, allocated):
    subnet, mask = cidr.split('/') # 1.2.3.4/24 => (1.2.3.4, 24)
    binary_ip = ip_to_bin(subnet)
    binary_mask = (pow(2, int(mask)) - 1) << (32 - int(mask)) # /24 => 11111111111111111111111100000000, 0b111111111111111111111111
    network = binary_ip & binary_mask # => 0000001000000100000001100000000
    hosts = pow(2, 32 - int(mask)) - 1 # => /24 => 255
    broadcast = network + hosts

    logger.debug("requested_ip: {}".format(requested_ip))

    if requested_ip:
        if ip_within_subnet(requested_ip, binary_mask, network):
            # Config provided IP
            if requested_ip in allocated:
                raise Exception("IP '{}' already used elsewhere.".format(requested_ip))
            else:
                allocated.append('{}'.format(requested_ip))
                return requested_ip
        else:
            raise Exception("""IP '{}' not valid ip within the network '{}'. Manually set the network, 
                or remove the ip address from the device to auto configure""".format(requested_ip, cidr))

    # Auto generated IP
    for ip in range(network + 1, broadcast - 1):
        dotIp = '{}.{}.{}.{}'.format((ip >> 24) & 0xff, (ip >> 16) & 0xff, (ip >> 8) & 0xff, ip & 0xff)
        if dotIp not in allocated:
            allocated.append(dotIp)
            return dotIp
    
    raise Exception('No more usable IP Addresses available in {}'.format(cidr))

def ip_to_bin(ip):
    octets = [int(octet) for octet in ip.split('.')] # 1.2.3.4 => [1, 2, 3, 4]
    return (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | (octets[0]) # [1, 2, 3, 4] => 0000001000000100000001100000100

def ip_within_subnet(ip, binary_mask, network):
    return (ip_to_bin(ip) & binary_mask) == network

def network_to_broadcat(network):
    subnet, mask = network.split('/') # 1.2.3.4/24 => (1.2.3.4, 24)
    binary_ip = ip_to_bin(subnet)
    binary_mask = (pow(2, int(mask)) - 1) << (32 - int(mask)) # /24 => 11111111111111111111111100000000, 0b111111111111111111111111
    network = binary_ip & binary_mask # => 0000001000000100000001100000000
    hosts = pow(2, 32 - int(mask)) - 1 # => /24 => 255
    broadcast = network + hosts
    return '{}.{}.{}.{}'.format((broadcast >> 24) & 0xff, (broadcast >> 16) & 0xff, (broadcast >> 8) & 0xff, broadcast & 0xff)

def random_uuid():
    return uuid.uuid1()