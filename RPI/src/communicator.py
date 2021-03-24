from abc import ABC, abstractmethod
import zmq
import time
import serial


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

    __inputs = {101: "Ping",
                103: "Ping",  # Error State Ping
                1: "Primary Motion",
                None: "Secondary Motion",  # TODO implement
                61: "Tertiary Motion",
                62: "Error String Disk",            # Error
                21: "Primary White",
                22: "Primary Black",
                23: "Primary Neither",              # Error
                41: "Secondary White",
                42: "Secondary Black",
                43: "Secondary Neither",            # Error
                11: "Confirm Blocker Extended",
                51: "Confirm Blocker Retracted",
                31: "Confirm Pusher Pushed",
                201: "White Set",
                203: "Black Set",
                205: "Initialization Finished",
                -1: "Unexpected Error Occurred",    # Error
                -2: "Illegal Command Sent",         # Error
                -3: "Unknown Command Sent",         # Error
                -4: "Message buffer full",          # Error
                -5: "Initialization Error"
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
                 "Finish Initialization": 204,
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

        # Check error mode
        if self._processor.get_error_mode():
            # Wait for user input to indicate that the issue fixed
            input('\033[91m' + "When the error has been fixed, press [ENTER]." + '\033[0m')

            # Unset error mode
            self._processor.set_error_mode(False)

            # Flush processor
            self._processor.flush()

            # Flush serial # TODO check if this is required
            self.serial.flush()

    def initialize(self):
        """
        Starts initialization process and calls self.start() when done
        """
        initialized = False
        while not initialized:
            # WHITE DISK
            input("Place white disks in front of the color sensors to calibrate them.\n" +
                  "When the disks are in place, press [ENTER].")
            self.serial.write(self.__outputs["Set White"])
            # wait for response
            if self.__wait_for_serial(10):
                # receive
                input_ = self.serial.readline().decode().rstrip()
            else:
                continue
            if not self.__is_correct_input(input_, "White Set"):
                continue

            # BLACK DISK
            input("Place black disks in front of the color sensors to calibrate them.\n" +
                  "When the disks are in place, press [ENTER].")
            self.serial.write(self.__outputs["Set Black"])
            # wait for response
            if self.__wait_for_serial(10):
                # receive
                input_ = self.serial.readline().decode().rstrip()
            else:
                continue
            if not self.__is_correct_input(input_, "Black Set"):
                continue

            # FINISH
            self.serial.write(self.__outputs["Finish Initialization"])
            # wait for response
            if self.__wait_for_serial(10):
                # receive
                input_ = self.serial.readline().decode().rstrip()
            else:
                continue
            if not self.__is_correct_input(input_, "Initialization Finished"):
                continue

            print("Initialization successfully completed, starting main process...")
            initialized = True
            self.start()

    def __wait_for_serial(self, time_out):
        """
        Checks if there is a message available on serial within given time.

        @param time_out  how many 1/10s of a second to wait before time out
        @returns whether a message was found before time out
        """

        time_out = time_out
        timer = 0
        # wait for response
        while self.serial.in_waiting == 0:
            if timer > time_out:
                print('\033[95m' + "No input received within expected time interval,"
                                   " initialization will restart." + '\033[0m')
                return False
            time.sleep(0.1)
            timer = timer + 1
        return True

    def __is_correct_input(self, input_, expected_input):
        """
        Returns whether expected input matches received input and prints error
        if this is not the case.

        @param input_  the received input
        @param expected_input  the expected input
        @returns @code{input_ == expected_input}
        """
        if input_ == self.__inputs["Initialization Error"]:
            print('\033[95m' + "Could not significantly distinguish black from white. "
                               "Please check whether the color sensors are in order "
                               "and there is no external light source interfering."
                               "Initialization process will restart." + '\033[0m')
            return False
        elif not input_ == self.__inputs[expected_input]:
            if input_ in self.__inputs:
                input_ = self.__inputs[input_]
            print('\033[95m' + "Unexpected input received: %s" % input_ + "Initialization will restart." + '\033[0m')
            return False
