class Processor:
    """
    Processes input and returns output for the communicator.

    Attributes
    __________
    __protocol_handler : ProtocolHandler
        An instance of the protocol handler to communicate with protocol

    __expectation_handler : ExpectationHandler
        An instance of the expectation handler to track expected inputs

    __stringer : Stringer
        An instance of a stringer to track the string status

    Methods
    _______
    set_stringer() : void
        Sets the stringer instance

    process(string) : string[*]
        Takes input, processes it, and returns output

    __ping() : string[*]
        Upon corresponding input, pings expectation handler and returns output

    __motion_detected() : string[*]
        Upon corresponding input, returns output

    __color_detected() : string[*]
        Upon corresponding input, returns output
    """

    def __init__(self, protocol_handler, expectation_handler):
        self.__protocol_handler = protocol_handler
        self.__expectation_handler = expectation_handler
        self.__stringer = None

    def set_stringer(self, stringer):
        """
        Sets the stringer for this processor object.
        @param stringer  Stringer to be set
        """

        self.__stringer = stringer

    def process(self, input):
        """
        Returns output after processing passed input.
        @param input  The input to be processed
        """

        if input == "Ping":
            return self.__ping()
        elif input == "Motion Detected":
            return self.__motion_detected()
        elif input == "White Detected":
            return self.__color_detected(0)
        elif input == "Black Detected":
            return self.__color_detected(1)
        else:
            return ["Unknown Message"]

    def __ping(self):
        """Returns output in case of ping."""

        self.__expectation_handler.ping()
        expired_outputs = self.__expectation_handler.get_expired_outputs()

        if expired_outputs:
            return expired_outputs
        else:
            return ["Pong"]

    def __motion_detected(self):
        """Returns output in case of motion."""

        if not self.__stringer.complete():
            # The stringer still needs disks
            self.__expectation_handler.add("Confirm Extend Blocker", ["Retract Blocker"], 10)
            return ["Extend Blocker", "Scan Color"]
        else:
            # The stringer does not need disks
            return ["Ignore"]

    def __color_detected(self, color):
        """
        Returns output in case of color.
        @param color  The color that was detected.
        """

        if not self.__stringer.should_pickup(color):
            # We do not want the color
            self.__expectation_handler.add("Confirm Retract Blocker", ["Extend Blocker"], 10)
            return ["Retract Blocker"]
        elif not self.__protocol_handler.can_pickup():
            # We are not allowed to pick up a disk
            return ["Retract Blocker"]
        else:
            # We want the color and we are allowed to pick up a disk
            return ["Push", "Retract Blocker"]
