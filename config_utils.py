#######
# Config files reader
#
# Module to read default and custom config files with the ability to provide best option for each property.
#######
import yaml

class config_values:
    defaultconfig = ""
    customconfig = ""

    def __init__(self):
        with open("config.yaml", 'r') as stream:
            try:
                self.defaultconfig = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        custom_filename = self.defaultconfig['custom_file_path']
        with open(custom_filename, 'r') as stream:
            try:
                self.customconfig = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        print("Config values loaded!")

    def get_best_value(self, property):
        value = self.customconfig[property]
        if not value:
            value = self.defaultconfig[property]
        return value
