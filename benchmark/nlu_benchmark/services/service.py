import os
import yaml


class Service:
    @classmethod
    def update_global_config(cls, **config):
        current_config = {}
        if os.path.isfile(cls.GLOBAL_CONFIG_FILE):
            stream = open(cls.GLOBAL_CONFIG_FILE, 'r')
            current_config = yaml.load(stream)
        current_config.update(config)
        stream = open(cls.GLOBAL_CONFIG_FILE, 'w+')
        stream.write(yaml.dump(current_config, default_flow_style=False))