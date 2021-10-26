#######
# MI Flora reader
#
# Module to interact with MI Flora devices using basnigholt/miflora and bluepy libraries
#######

# miflora poller info at https://github.com/basnijholt/miflora
import logging
from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from miflora import miflora_scanner
from btlewrap.bluepy import BluepyBackend

FIRMWARE = "Firmware"
MOISTURE = "Moisture"
TEMPERATURE = "Temperature"
LIGHT = "Light"
FERTILIZER = "Fertilizer"
BATTERY = "Battery"

DEMO_MESSAGE = "DEMO mode is active"

log = logging.getLogger(__name__)
mode = ''

def connect(mac, run_mode):
    poller = None
    global mode 
    mode = run_mode
    if mode != 'DEMO':
        poller = MiFloraPoller(mac, BluepyBackend)
    else: 
        log.warning(DEMO_MESSAGE)

    return poller

def scan(run_mode):
    log.info('Looking for MiFlora devices...')
    if (run_mode != 'DEMO'):
        devices = miflora_scanner.scan(BluepyBackend, 10)
        log.info('Found {} devices:'.format(len(devices)))
        for device in devices:
            log.info('  {}'.format(device))
    else:
        log.warning(DEMO_MESSAGE)

def poll(poller):
    log.debug("Starting poll")
    device_info = {}
    if (mode != 'DEMO'):
        device_info[FIRMWARE] = poller.firmware_version()
        device_info[TEMPERATURE] = poller.parameter_value(MI_TEMPERATURE)
        device_info[MOISTURE] = poller.parameter_value(MI_MOISTURE)
        device_info[LIGHT] = poller.parameter_value(MI_LIGHT)
        device_info[FERTILIZER] = poller.parameter_value(MI_CONDUCTIVITY)
        device_info[BATTERY] = poller.parameter_value(MI_BATTERY)
    else:
        log.warning(DEMO_MESSAGE)
        device_info[FIRMWARE] = 1
        device_info[TEMPERATURE] = 10
        device_info[MOISTURE] = 10
        device_info[LIGHT] = 1
        device_info[FERTILIZER] = 1
        device_info[BATTERY] = 1
    log.debug("Ending poll" + str(device_info))
    return device_info

