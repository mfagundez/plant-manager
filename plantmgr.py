#######
# Plant manager
#
# Main module to scan each device in order to read its properties.
#######

import miflora_utils
import config_utils
import mail_sender
import logging

log = logging.getLogger(__name__)

PARAMS = "PARAMS"
DATA = "DATA"

# check if value received is between allowed range for the device and param provided
def valid_value(device, param, value):
    if ((device[param][config_utils.CHECK])
    and ((device[param][config_utils.HIGH] < value)
        or (device[param][config_utils.LOW] >= value))):
        log.warning("alert " + param + " out of range")
        return False
    else:
        return True

# prepare the body message with html format. Firstly prints the 
# devices that need to be reviewed, then the unknown due to connection problems
# and finally the other ones.
def prepare_mail_message(devices_in_error, devices_ok, devices_unknown):
    if (len(devices_in_error) > 0):
        message = "<p>Following plants need to be reviewed: </p><p><ul>" 
        error_keys = devices_in_error.keys()
        for error_key in error_keys:
            data = devices_in_error[error_key][DATA]
            params = devices_in_error[error_key][PARAMS]
            message = message + "<li><b>" + error_key + "</b>: <u>"+ str(params) +"</u> | <i> data :: " + str(data) + "</i></li>"
        message = message + "</ul></p>"

    if (len(devices_unknown) > 0):
        message = message + "<p>Following devices are unreachables: </p><p><ul>" 
        for device_unknown in devices_unknown:
            message = message + "<li><b>" + device_unknown + "</b></li>"
        message = message + "</ul></p>"

    if (len(devices_ok) > 0):
        message = message + "<p>Anyway, here are the params for the rest of the plants: </p><p><ul>" 
        ok_keys = devices_ok.keys()
        for ok_key in ok_keys:
            message = message + "<li><b>" + ok_key + "</b>: <i>" + str(devices_ok[ok_key]) + "</i></li>"
        message = message + "</ul></p>"
    return message



configreader = config_utils.config_values()
loglevel = configreader.get_best_value(config_utils.LOGLEVEL)
logging.basicConfig(level=loglevel,format='%(asctime)s %(levelname)s %(name)s %(message)s')

mode = configreader.get_best_value(config_utils.MODE)
devices = configreader.get_best_value(config_utils.DEVICES)

# mail sender init. with api key & secret
smtp = configreader.get_best_value(config_utils.SMTPINFO)
mailsender = mail_sender.mail_sender(smtp[config_utils.APIKEY], smtp[config_utils.APISECRET])

# it will contain each device whose has at least one param out of range, and all values read from device.
devices_in_error = dict()
# it will contain each device whose all parameters fit into ranges
devices_ok = dict()
# it will contain each device with connection issues
devices_unknown = list()

for device in devices:
    read_data = dict()
    params_to_review = list()
    mac = device[config_utils.MAC]
    log.info("==> Device: " + device[config_utils.NAME] + "["+ mac + "]")
    # connect and get data from device
    try:
        poller = miflora_utils.connect(mac, mode)
        device_info = miflora_utils.poll(poller)

        # get values from read data
        read_data[config_utils.MOISTURE] = device_info[miflora_utils.MOISTURE]
        read_data[config_utils.TEMP] = device_info[miflora_utils.TEMPERATURE]
        read_data[config_utils.LIGHT] = device_info[miflora_utils.LIGHT]
        read_data[config_utils.FERTILITY] = device_info[miflora_utils.FERTILIZER]
        read_data[config_utils.BATTERY] = device_info[miflora_utils.BATTERY]
        read_data[config_utils.FIRMWARE] = device_info[miflora_utils.FIRMWARE]

        # check values if enabled, adding device to dict if any param is not valid
        if (not valid_value(device, config_utils.MOISTURE, read_data[config_utils.MOISTURE])):
            params_to_review.append(config_utils.MOISTURE)
        if (not valid_value(device, config_utils.TEMP, read_data[config_utils.TEMP])):
            params_to_review.append(config_utils.TEMP)
        if (not valid_value(device, config_utils.LIGHT, read_data[config_utils.LIGHT])):
            params_to_review.append(config_utils.LIGHT)
        if (not valid_value(device, config_utils.FERTILITY, read_data[config_utils.FERTILITY])):
            params_to_review.append(config_utils.FERTILITY)
        if (not valid_value(device, config_utils.BATTERY, read_data[config_utils.BATTERY])):
            params_to_review.append(config_utils.BATTERY)

        if (len(params_to_review) > 0):
            device_to_review = dict()
            device_to_review[PARAMS] = params_to_review
            device_to_review[DATA] = read_data
            devices_in_error[device[config_utils.NAME]] = device_to_review
        else:
            devices_ok[device[config_utils.NAME]] = read_data
    except Exception:
        # catch any exception (usually due to connection issues)
        log.error("An error occurred while connecting to " + device[config_utils.NAME] + "["+ mac + "]",exc_info=True)
        devices_unknown.append(device[config_utils.NAME])

# Mail is sent just if any device is out of range, but including all data for information purposes
if(len(devices_in_error) > 0):
    message = prepare_mail_message(devices_in_error, devices_ok, devices_unknown)
    log.debug("message to send = " + message)
    mail_info = configreader.get_best_value(config_utils.MAILINFO)
    if (mode != 'DEMO'):
        mailsender.send_email(smtp[config_utils.SENDERMAIL], smtp[config_utils.SENDERNAME], 
            mail_info[config_utils.MAILTO], mail_info[config_utils.MAILCC], mail_info[config_utils.MAILBCC], 
            mail_info[config_utils.MAILSUBJECT], message)
        log.debug("Sending complete!")
    else:
        log.warning("DEMO mode is active")
else:
    log.debug("Any plant is in error status!")