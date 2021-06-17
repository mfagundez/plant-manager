#######
# MI Flora reader
#
# Module to interact with MI Flora devices using basnigholt/miflora and bluepy libraries
#######

# miflora poller info at https://github.com/basnijholt/miflora
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from miflora import miflora_scanner
from btlewrap.bluepy import BluepyBackend

FIRMWARE = "Firmware"
MOISTURE = "Moisture"
TEMPERATURE = "Temperature"
LIGHT = "Light"
FERTILIZER = "Fertilizer"
BATTERY = "Battery"

def connect(mac):
    return MiFloraPoller(mac, BluepyBackend)

def scan():
    print('Looking for MiFlora devices...')
    devices = miflora_scanner.scan(BluepyBackend, 10)
    print('Found {} devices:'.format(len(devices)))
    for device in devices:
        print('  {}'.format(device))

def poll(poller):
    device_info = {}
    device_info[FIRMWARE] = poller.firmware_version()
    device_info[TEMPERATURE] = poller.parameter_value(MI_TEMPERATURE)
    device_info[MOISTURE] = poller.parameter_value(MI_MOISTURE)
    device_info[LIGHT] = poller.parameter_value(MI_LIGHT)
    device_info[FERTILIZER] = poller.parameter_value(MI_CONDUCTIVITY)
    device_info[BATTERY] = poller.parameter_value(MI_BATTERY)
    return device_info

