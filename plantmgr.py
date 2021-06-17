#######
# Plant manager
#
# Main module to scan each device in order to read its properties.
#######

import miflora_utils
import config_utils

# check if value received is between allowed range for the device and param provided
def valid_value(device, param, value):
    if ((device[param][config_utils.CHECK])
    and ((device[param][config_utils.HIGH] < value)
        or (device[param][config_utils.LOW] >= value))):
        print("alert " + param)
        return False
    else:
        return True

configreader = config_utils.config_values()
devices = configreader.get_best_value(config_utils.DEVICES)

# it will contain each device who has at least one param out of range, and all values read from device.
devices_in_error = dict()

for device in devices:
    read_data = dict()
    mac = device[config_utils.MAC]
    print('==> MAC:' + mac)
    # connect and get data from device
    poller = miflora_utils.connect(mac)
    device_info = miflora_utils.poll(poller)
    # get values from read data
    read_data[config_utils.MOISTURE] = device_info[miflora_utils.MOISTURE]
    read_data[config_utils.TEMP] = device_info[miflora_utils.TEMPERATURE]
    read_data[config_utils.LIGHT] = device_info[miflora_utils.LIGHT]
    read_data[config_utils.FERTILITY] = device_info[miflora_utils.FERTILIZER]
    read_data[config_utils.BATTERY] = device_info[miflora_utils.BATTERY]

    # check values if enabled, adding device to dict if any param is not valid
    if ((not valid_value(device, config_utils.MOISTURE, read_data[config_utils.MOISTURE]))
    or (not valid_value(device, config_utils.TEMP, read_data[config_utils.TEMP]))
    or (not valid_value(device, config_utils.LIGHT, read_data[config_utils.LIGHT]))
    or (not valid_value(device, config_utils.FERTILITY, read_data[config_utils.FERTILITY]))
    or (not valid_value(device, config_utils.BATTERY, read_data[config_utils.BATTERY]))):
        devices_in_error[device[config_utils.NAME]] = read_data

print(devices_in_error)
