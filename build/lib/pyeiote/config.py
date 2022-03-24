from utils import load_yaml
import json

class DotConfig(object):

    def __new__(cls, cfg):
        return super(DotConfig, cls).__new__(cls)
    
    def __init__(self, cfg):
        self.cfg = cfg
    
    def __getattr__(self, key):
        try:
            value = self.cfg[key]
        except:
            return None
        
        if isinstance(value, dict):
            return DotConfig(value)
        if isinstance(value, list):
            return map(lambda v: DotConfig(v), value)
        return value
    
    def __str__(self):
        return json.dumps(self.cfg)

class Config(object):

    """
    def __new__(self):
        self.cfg = load_yaml("./config.yaml")
        return DotConfig(self.cfg)
    """
    def __new__(self, config_file):
        return load_yaml(config_file)

    