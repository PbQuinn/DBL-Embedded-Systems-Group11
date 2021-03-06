from abc import ABC, abstractmethod
import zmq
import time
import serial

DEVICE_NAME = '[Enter Device Name Here]'    # TODO add actual device name


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
        if input_ != "Ping":
            print('\033[96m' + "Received: %s" % input_ + '\033[0m')

        # Process
        output = ",".join(self._processor.process(input_)).encode()

        # Send
        self.__socket.send(output)
        if output != b"Pong":
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
                103: "Error Ping",  # Error State Ping
                1: "Primary Motion",
                2: "Secondary Motion",
                61: "Tertiary Motion",
                62: "Error String Disk",            # Error
                21: "Primary White",
                22: "Primary Black",
                23: "Primary Neither",
                41: "Secondary White",
                42: "Secondary Black",
                43: "Secondary Neither",            # Error
                11: "Confirm Blocker Extended",
                51: "Confirm Blocker Retracted",
                31: "Confirm Pusher Pushed",
                201: "White Set",
                203: "Black Set",
                205: "Initialization Finished",
                254: "Unexpected Error Occurred",    # Error
                253: "Illegal Command Sent",         # Error
                252: "Unknown Command Sent",         # Error
                251: "Message Buffer Full",          # Error
                250: "Initialization Error",         # Error
                105: "Error Mode Exited"
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
                 "Enter Error Mode": 102,
                 "Exit Error Mode": 104,
                 "Ignore": None
                 }

    def __init__(self, processor, device_name=DEVICE_NAME):
        # Call super constructor
        Communicator.__init__(self, processor)
        # Initialize serial
        self.serial = serial.Serial(device_name, 9600, timeout=1)
        self.serial.flush()
        # Ping counter (mod 10)
        self.ping_counter = 0

    def _communicate(self):

        # Receive
        if self.serial.in_waiting > 0:
            input_ = int.from_bytes(self.serial.read(), byteorder='big')
            if input_ not in self.__inputs:
                print('\033[91m' + "Unexpected input received from Arduino: %s"
                      % input_ + '\033[0m')
                input_ = "Unexpected Error Occurred"
            else:
                if self.__inputs[input_] == "Ping":
                    if self.ping_counter >= 10:
                        self.ping_counter = 0
                        print('\033[96m' + "Received: %s" % input_ + "= %s"
                              % self.__inputs[input_] + '\033[0m')
                    else:
                        self.ping_counter = self.ping_counter + 1
                else:
                    print('\033[96m' + "Received: %s" % input_ + "= %s"
                          % self.__inputs[input_] + '\033[0m')
                input_ = self.__inputs[input_]

            # Process
            outputs = self._processor.process(input_)

            # Send
            for output in outputs:
                output = self.__outputs[output]
                if output is not None:
                    self.serial.write((str(output)+"\n").encode('utf-8'))
                    if output != 100:
                        print('\033[95m' + "Sent: %s" % output + '\033[0m')

        # Check error mode
        if self._processor.get_error_mode():
            # Wait for user input to indicate that the issue fixed
            input('\033[91m' + "When the error has been fixed, press [ENTER]." + '\033[0m')

            # Unset error mode
            self._processor.set_error_mode(False)

            # Flush processor
            self._processor.flush()

            # Flush serial
            self.__flush()

            # Exit Error Mode
            self.serial.write((str(self.__outputs["Exit Error Mode"]) + "\n").encode('utf-8'))

    def initialize(self):
        """
        Starts initialization process and calls self.start() when done
        """

        initialized = False
        while not initialized:
            self.__flush()
            # WHITE DISK
            input("Place white disks in front of the color sensors to calibrate them.\n" +
                  "When the disks are in place, press [ENTER].")
            self.serial.write((str(self.__outputs["Set White"]) + "\n").encode('utf-8'))
            # wait for response
            if self.__wait_for_serial(100):
                # receive
                input_ = int.from_bytes(self.serial.read(), byteorder='big')
            else:
                continue
            if not self.__is_correct_input(input_, 201):
                continue

            # BLACK DISK
            input("Place black disks in front of the color sensors to calibrate them.\n" +
                  "When the disks are in place, press [ENTER].")
            self.serial.write((str(self.__outputs["Set Black"]) + "\n").encode('utf-8'))
            # wait for response
            if self.__wait_for_serial(100):
                # receive
                input_ = int.from_bytes(self.serial.read(), byteorder='big')
            else:
                continue
            if not self.__is_correct_input(input_, 203):
                continue

            start_robot = input("Initialization successfully completed. Type 'r' to restart,"
                                "\nor install the string and press anything else to start te robot.")
            if str(start_robot) == "r":
                continue

            # FINISH
            self.serial.write((str(self.__outputs["Finish Initialization"]) + "\n").encode('utf-8'))
            # wait for response
            if self.__wait_for_serial(30):
                # receive
                input_ = int.from_bytes(self.serial.read(), byteorder='big')
            else:
                continue
            if not self.__is_correct_input(input_, 205):
                continue

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
                input('\033[95m' + "No input received within expected time interval,"
                                   "\nPress [ENTER] to restart the calibration process." + '\033[0m')
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

        if input_ == 250:
            input('\033[95m' + "Could not significantly distinguish black from white. "
                               "Please check whether the color sensors are in order "
                               "and there is no external light source interfering."
                               "\nPress [ENTER] to restart te calibration process." + '\033[0m')
            return False
        elif not input_ == expected_input:
            if input_ in self.__inputs:
                input_ = self.__inputs[input_]
            print('\033[95m' + "Unexpected input received: %s" % input_ +
                  "\nInitialization process will restart." + '\033[0m')
            return False
        else:
            return True

    def __flush(self):
        """
        Flushes the serial
        """

        while self.serial.in_waiting > 0:
            int.from_bytes(self.serial.read(), byteorder='big')
