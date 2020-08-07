

from miflora.miflora_poller import MiFloraPoller
from btlewrap.pygatt import PygattBackend

poller = MiFloraPoller('some mac address', PygattBackend)
