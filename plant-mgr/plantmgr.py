

from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend

poller = MiFloraPoller('some mac address', BluepyBackend)

print("hola miFlora. El nivel de bateria es: " + poller.battery_level)