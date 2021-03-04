from abc import ABC, abstractmethod


class DiskPusher(ABC):
    """Interface used to interact with pusher
    """

    def __init__(self):
        self.pusher_interface = None


class ArduinoDiskPusher(DiskPusher):
    """Concrete disk pusher interface used for interacting with arduino
    """


class UnityDiskPusher(DiskPusher):
    """Concrete disk pusher interface used for interacting with simulation
    """

# TODO implement communication with arduino / simulation
