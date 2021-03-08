from abc import ABC, abstractmethod


class DiskPusher(ABC):
    """Interface used to interact with pusher
    """

    def __init__(self):
        pass

    @abstractmethod
    def pulse(self):
        """Checks if pusher is still alive
        """

        pass

    @abstractmethod
    def get_data(self):
        """Reads data from pusher if available
        """

        pass

    @abstractmethod
    def close_gate(self):
        """Sends signal to pusher to close the gate
        """

        pass

    @abstractmethod
    def open_gate(self):
        """Sends signal to pusher to close the gate
        """

        pass

    @abstractmethod
    def get_color(self):
        """Returns the color of the incoming disk
        """

        pass

    @abstractmethod
    def push_disk(self):
        """Sends signal to pusher to push disk
        """

        pass


class ArduinoDiskPusher(DiskPusher):
    """Concrete disk pusher interface used for interacting with arduino
    """


class UnityDiskPusher(DiskPusher):
    """Concrete disk pusher interface used for interacting with simulation
    """

# TODO implement communication with arduino / simulation
