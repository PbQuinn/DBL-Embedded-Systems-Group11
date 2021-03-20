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

        if output == b"Error Occurred":
            input('\033[91m' + "When the error has been fixed, press [ENTER]." + '\033[0m')


class CommunicatorRobot(Communicator):
    """Concrete communicator class for robot."""

    __inputs = {101: "Ping",
                103: "Ping",  # Error State Ping
                1: "Primary Motion",
                # 1: "Secondary Motion",
                61: "Tertiary Motion",
                62: "Error Occurred",  # Error String Disk
                21: "Primary White",
                22: "Primary Black",
                23: "Primary Neither",
                41: "Secondary White",
                42: "Secondary Black",
                43: "Secondary Neither",
                11: "Confirm Blocker Extended",
                51: "Confirm Blocker Retracted",
                31: "Confirm Pusher Pushed",
                201: "White Set",
                203: "Black Set",
                -1: "Error Occurred",  # Unexpected Error
                -2: "Error Occurred",  # Illegal Command
                -3: "Error Occurred",  # Unknown Command
                -4: "Error Occurred",  # Buffer Full
                107: "Start Error Message",
                108: "End Error Message"}

    __outputs = {"Pong": 100,
                 "Scan Primary Color": 20,
                 "Scan Secondary Color": 40,
                 "Extend Blocker": 10,
                 "Retract Blocker": 50,
                 "Push Pusher": 30,
                 "Push Stringer": 60,
                 "Set White": 200,
                 "Set Black": 202,
                 "Enter Error State": 102,
                 "Exit Error State": 104,
                 "Get Error State Info": 106,
                 "Ignore": None
                 }

    def __init__(self, processor):
        # Call super constructor
        Communicator.__init__(self, processor)


    def _communicate(self):
        # Receive

        # Process

        # Send
        
        pass
