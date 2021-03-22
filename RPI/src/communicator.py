from abc import ABC, abstractmethod
import zmq
import serial  # TODO import serial into virtual environment (https://pypi.org/project/pyserial/)


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
                None: "Secondary Motion",  # TODO implement
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
                # 107: "Start Error Message",
                # 108: "End Error Message"
                }

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

    def __init__(self, processor, device_name="VeryCoolName"):  # TODO add actual device name
        # Call super constructor
        Communicator.__init__(self, processor)
        # Initialize serial
        self.serial = serial.Serial(device_name, 9600, timeout=1)
        self.serial.flush()

    def _communicate(self):

        # Receive
        if self.serial.in_waiting > 0:
            input_ = self.serial.readline().decode().rstrip()
            if input_ not in self.__inputs:
                print('\033[91m' + "Unexpected input received from Arduino: %s"
                      % input_ + '\033[0m')
                input_ = "Error Occurred"
            else:
                print('\033[96m' + "Received: %s" % input_ + "= %s"
                      % self.__inputs[input_] + '\033[0m')
                input_ = self.__inputs[input_]

            # Process
            output = self._processor.process(input_)

            # Send
            output = self.__outputs[output]
            if output is not None:
                self.serial.write(output)
            print('\033[95m' + "Sent: %s" % output + '\033[0m')

    def initialize(self):
        initialized = False
        while not initialized:
            input("Place white disks in front of the color sensors to calibrate them.\n" +
                  "When the disks are in place, press [ENTER].")
            self.serial.write(self.__outputs["Set White"])
            # wait for response
            while self.serial.in_waiting == 0:
                pass
            # receive
            input_ = self.serial.readline().decode().rstrip()
            if not input_ == self.__inputs["White Set"]:
                print('\033[95m' + "Something went wrong, initialization will restart." + '\033[0m')
                continue

            input("Place black disks in front of the color sensors to calibrate them.\n" +
                  "When the disks are in place, press [ENTER].")
            self.serial.write(self.__outputs["Set Black"])
            # wait for response
            while self.serial.in_waiting == 0:
                pass
            # receive
            input_ = self.serial.readline().decode().rstrip()
            if not input_ == self.__inputs["Black Set"]:
                print('\033[95m' + "Something went wrong, initialization will restart." + '\033[0m')
                continue

            print("Initialization successfully completed, starting main process...")
            initialized = True
            self.start()
