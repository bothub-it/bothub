import os
import yaml


class Service:
    @classmethod
    def get_current_global_config(cls):
        current_config = {}
        if os.path.isfile(cls.GLOBAL_CONFIG_FILE):
            stream = open(cls.GLOBAL_CONFIG_FILE, 'r')
            current_config = yaml.load(stream)
        return current_config

    @classmethod
    def update_global_config(cls, **config):
        current_config = cls.get_current_global_config()
        current_config.update(config)
        stream = open(cls.GLOBAL_CONFIG_FILE, 'w+')
        stream.write(yaml.dump(current_config, default_flow_style=False))
