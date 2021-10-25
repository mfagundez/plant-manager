#######
# Config files reader
#
# Module to read default and custom config files with the ability to provide best option for each property.
#######
import logging
import yaml

LOGLEVEL = "log_level"
SMTPINFO = "smtp_info"
APIKEY = "apikey"
APISECRET = "apisecret"
SENDERMAIL = "sender_mail"
SENDERNAME = "sender_name"
MAILINFO = "mail_info"
MAILTO = "to"
MAILCC = "cc"
MAILBCC = "bcc"
MAILSUBJECT = "subject"
DEVICES = "devices"
CUSTOM_FILE_PATH = "custom_file_path"
MAC = "mac"
NAME = "name"
MOISTURE = "moisture"
FERTILITY = "fertility"
LIGHT = "light"
TEMP = "temp"
BATTERY = "battery"
CHECK = "check"
HIGH = "high"
LOW = "low"

class config_values:
    defaultconfig = ''
    customconfig = ''
    log = logging.getLogger(__name__)

    def __init__(self):
        with open("config.yaml", 'r') as stream:
            try:
                self.defaultconfig = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                self.log.critical(exc)
                raise

        custom_filename = self.defaultconfig[CUSTOM_FILE_PATH]
        with open(custom_filename, 'r') as stream:
            try:
                self.customconfig = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                self.log.warn("Custom file not found: " + str(exc))

        self.log.info("Config values loaded!")

    def get_best_value(self, property):
        try:
            value = self.customconfig[property]
        except Exception:
            value = None
        if not value:
            value = self.defaultconfig[property]
        self.log.debug("read value for " + property + ": " + str(value))
        return value
