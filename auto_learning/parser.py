import configparser

class ConfigParser:

    config = configparser.ConfigParser()

    def __init__(self, config_file):
        self.config.read(config_file)

    def get_setting(self, section, property):
        return self.config[section][property]