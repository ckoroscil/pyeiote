from .device_profiles.device import Device
from .config import Config
from .utils import generate_network, get_ip_address
import logging
import os
import time
import signal
import argparse

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger('eiot-traffic-gen')

threads = []

def is_any_thread_alive():
    return True in [t.is_alive() for t in threads]

def sigint_handler(signum, frame):
    logger.info("ctrl-c. Stopping all child threads...")
    for thread in threads:
        thread.stop()
        thread.join(1)

parser = argparse.ArgumentParser(description='Generate Enterprise IoT traffic.')
parser.add_argument('--debug', action='store_true', help='show debug messages')
parser.add_argument('-i', '--interface', type=str, help='the network interface where packets should go', required=True)
args = parser.parse_args()

os.environ["SCAPYIFACE"] = args.interface

logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

signal.signal(signal.SIGINT, sigint_handler)

config_file = "./config.yaml"
logger.info('loading {}'.format(config_file))
config = Config(config_file)

networks = config.get('networks', [])
if len(networks) == 0: raise Exception("missing 'networks' block within {}".format(config_file))

for network_config in networks:
    allocated_ips = []
    network = generate_network(network_config)
    logger.debug('processing network: {}'.format(network_config))

    for device in networks[network_config].get('devices', []):
        logger.debug('processing device: {}'.format(device))
        device['network'] = network
        requested_ip = device.get('ipv4', None)
        device['ipv4'] = get_ip_address(network, requested_ip, allocated_ips)
        device = Device(device)
        device.start()
        threads.append(device)

logger.info('Running...')

while is_any_thread_alive():
    time.sleep(0)
