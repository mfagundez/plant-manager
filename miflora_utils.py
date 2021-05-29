#######
# MI Flora reader
#
# Module to interact with MI Flora devices using basnigholt/miflora and bluepy libraries
#######

# miflora poller info at https://github.com/basnijholt/miflora
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from miflora import miflora_scanner
from btlewrap.bluepy import BluepyBackend

def connect(mac):
    return MiFloraPoller(mac, BluepyBackend)

def scan():
    print('Looking for MiFlora devices...')
    devices = miflora_scanner.scan(BluepyBackend, 10)
    print('Found {} devices:'.format(len(devices)))
    for device in devices:
        print('  {}'.format(device))

def poll(poller):
    print("Firmware: {}".format(poller.firmware_version()))
    print("Temperature: {}".format(poller.parameter_value(MI_TEMPERATURE)))
    print("Moisture: {}".format(poller.parameter_value(MI_MOISTURE)))
    print("Light: {}".format(poller.parameter_value(MI_LIGHT)))
    print("Fertilizer: {}".format(poller.parameter_value(MI_CONDUCTIVITY)))
    print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))
