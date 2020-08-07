

from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend

poller = MiFloraPoller('some mac address', BluepyBackend)