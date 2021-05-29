#######
# Plant manager
#
# Main module to scan each device in order to read its properties.
#######

import miflora_utils
import config_utils

configreader = config_utils.config_values()
devices = configreader.get_best_value('devices')

for device in devices:
    mac = device['mac']
    print('==> MAC:' + mac)
    poller = miflora_utils.connect(mac)
    miflora_utils.poll(poller)
    print('\n')