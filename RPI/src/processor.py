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
    process(string) : string[*]
        Takes input, processes it, and returns output

    __ping() : string[*]
        Upon corresponding input, pings expectation handler and returns output

    __motion_detected() : string[*]
        Upon corresponding input, returns output

    __color_detected() : string[*]
        Upon corresponding input, returns output
    """

    def __init__(self, stringer, protocol_handler, expectation_handler):
        self.__stringer = stringer
        self.__protocol_handler = protocol_handler
        self.__expectation_handler = expectation_handler

    def process(self, input_):
        """
        Returns output after processing passed input.
        @param input_  The input to be processed
        """

        # Main interactions:
        if input_ == b"Ping":
            return self.__ping()
        elif input_ == b"Motion Detected":
            return self.__motion_detected()
        elif input_ == b"White Detected":
            return self.__color_detected(0)
        elif input_ == b"Black Detected":
            return self.__color_detected(1)
        elif input_ == b"Confirm Blocker Extended":
            return self.__blocker_extended()
        elif input_ == b"Confirm Blocker Retracted":
            return self.__blocker_retracted()
        elif input_ == b"Confirm Pusher Push":
            return self.__pusher_pushed()
        elif input_ == b"Confirm Stringer Push":
            return self.__disk_stringed()

        # Startup interactions:
        elif input_ == b"White Set":
            pass    # TODO implement
        elif input_ == b"Black Set":
            pass    # TODO implement

        # Error interactions:
        elif input_ == b"Error Occurred":
            pass    # TODO implement
        else:
            return [b"Unknown Message"]

    def __ping(self):
        """Returns output in case of ping."""

        self.__expectation_handler.ping()
        expired_outputs = self.__expectation_handler.get_expired_outputs()
        return [b"Pong"] + expired_outputs

    def __motion_detected(self):
        """Returns output in case of motion."""

        if not self.__stringer.is_complete():
            # The stringer still needs disks
            self.__expectation_handler.add(b"Confirm Blocker Extended",
                                           [b"Retract Blocker"], 10)
            return [b"Extend Blocker"]
        else:
            # The stringer does not need disks
            return [b"Ignore"]

    def __color_detected(self, color):
        """
        Removes expectation and returns output in case of color.
        @param color  The color that was detected.
        """

        self.__expectation_handler.remove(b"Color Detected")

        if not self.__stringer.should_pickup(color):
            # We do not want the color
            self.__expectation_handler.add(b"Confirm Blocker Retracted",
                                           [b"Extend Blocker"], 10)
            return [b"Retract Blocker"]
        elif not self.__protocol_handler.can_pickup():
            # We are not allowed to pick up a disk
            self.__expectation_handler.add(b"Confirm Blocker Retracted",
                                           [b"Extend Blocker"], 10)
            return [b"Retract Blocker"]
        else:
            # We want the color and we are allowed to pick up a disk
            self.__expectation_handler.add(b"Confirm Pusher Push", [], 10)
            return [b"Push"]

    def __blocker_extended(self):
        """
        Removes expectation and returns output in case of blocker extended.
        """

        self.__expectation_handler.remove(b"Confirm Blocker Extended")
        self.__expectation_handler.add(b"Color Detected", [], 10)
        return [b"Scan Color"]

    def __blocker_retracted(self):
        """
        Removes expectation in case of blocker retracted.
        """

        self.__expectation_handler.remove(b"Confirm Blocker Retracted")

    def __pusher_pushed(self):
        """
        Removes expectation and returns output in case of pusher pushed.
        """

        self.__expectation_handler.remove(b"Confirm Pusher Push")
        self.__expectation_handler.add(b"Confirm Blocker Retracted", [b"Extend Blocker"])
        return [b"Retract Blocker"]

    def __disk_stringed(self):
        """
        Removes expectation in case of disk stringed.
        """

        self.__expectation_handler.remove(b"Confirm Stringer Push")
