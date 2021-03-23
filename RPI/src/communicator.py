from abc import ABC, abstractmethod
import zmq


class Communicator(ABC):
    """Abstract communicator class."""

    def __init__(self, processor):
        self._processor = processor
        self._running = False

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
        self.__socket = context.socket(zmq.REP)
        self.__socket.bind("tcp://*:5555")

    def _communicate(self):
        # Receive
        input_ = self.__socket.recv_string()
        print('\033[96m' + "Received: %s" % input_ + '\033[0m')

        # Process
        output = ",".join(self._processor.process(input_)).encode()

        # Send
        self.__socket.send(output)
        print('\033[95m' + "Sent: %s" % output + '\033[0m')

        if self._processor.get_error_mode():
            # Wait for user input to indicate that the issue fixed
            input('\033[91m' + "When the error has been fixed, press enter any key." + '\033[0m')

            # Unset error mode
            self._processor.set_error_mode(False)

            # Flush processor
            self._processor.flush()

            # Close current socket
            self.__socket.close()

            # Create and bind new socket
            context = zmq.Context()
            self.__socket = context.socket(zmq.REP)
            self.__socket.bind("tcp://*:5555")


class CommunicatorRobot(Communicator):
    """Concrete communicator class for robot."""

    def __init__(self, processor):
        Communicator.__init__(self, processor)

    def _communicate(self):
        pass
