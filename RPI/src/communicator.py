from abc import ABC, abstractmethod
import zmq


class Communicator(ABC):
    """Abstract communicator class."""

    """The processor the communicator will use to process received messages."""
    _processor = None

    """Whether the communicator is running."""
    _running = False

    def __init__(self, processor):
        self._processor = processor

    def start(self):
        """Start communicating."""

        self._running = True

        while self._running:
            self._communicate()

    def stop(self):
        """Stop communicating."""

        self._running = False

    def get_running(self):
        """Return whether the communicator is running."""

        return self._running

    @abstractmethod
    def _communicate(self):
        """Communicate (abstract)."""

        pass


class CommunicatorSimulation(Communicator):
    """Concrete communicator class for simulation."""

    def __init__(self, processor):
        # Call super constructor
        Communicator.__init__(self, processor)

        # Create and bind socket
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

    def _communicate(self):
        # Receive
        msg_receive = self.socket.recv()
        print("Received: %s" % msg_receive)

        # Process
        msg_send = self._processor.process(msg_receive)

        # Send
        self.socket.send(msg_send)
        print("Sent: %s" % msg_send)


class CommunicatorRobot(Communicator):
    """Concrete communicator class for robot."""

    def __init__(self, processor):
        Communicator.__init__(self, processor)

    def _communicate(self):
        pass
