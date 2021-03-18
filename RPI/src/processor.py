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

        try:
            # Main interactions:
            if input_ == "Ping":
                return self.__ping()
            elif input_ == "Motion Detected":
                return self.__motion_detected()
            elif input_ == "Primary White":
                return self.__primary_color_detected(0)
            elif input_ == "Primary Black":
                return self.__primary_color_detected(1)
            elif input_ == "Secondary White":
                return self.__secondary_color_detected(0)
            elif input_ == "Secondary Black":
                return self.__secondary_color_detected(1)
            elif input_ == "Confirm Blocker Extended":
                return self.__blocker_extended()
            elif input_ == "Confirm Blocker Retracted":
                return self.__blocker_retracted()
            elif input_ == "Confirm Pusher Push":
                return self.__pusher_pushed()
            elif input_ == "Confirm Stringer Push":
                return self.__disk_stringed()

            # Startup interactions:
            elif input_ == "White Set":
                pass    # TODO implement
            elif input_ == "Black Set":
                pass    # TODO implement

            # Error interactions:
            elif input_ == "Error Occurred":
                pass    # TODO implement
            else:
                return ["Unknown Message"]
        except Exception:
            # TODO add error handling code
            pass

    def __ping(self):
        """Returns output in case of ping."""

        self.__expectation_handler.ping()
        self.__protocol_handler.inform_alive()
        expired_outputs = self.__expectation_handler.get_expired_outputs()
        return ["Pong"] + expired_outputs

    def __motion_detected(self):
        """Returns output in case of motion."""

        if not self.__stringer.is_complete():
            # The stringer still needs disks
            self.__expectation_handler.add("Confirm Blocker Extended",
                                           ["Retract Blocker"], 10)    # TODO adjust timer
            return ["Extend Blocker"]
        else:
            # The stringer does not need disks
            return ["Ignore"]

    def __primary_color_detected(self, color):
        """
        Removes expectation and returns output in case of color.
        @param color  The color that was detected.
        """

        self.__expectation_handler.remove("Primary Color Detected")

        if not self.__stringer.should_pickup(color):
            # We do not want the color
            self.__expectation_handler.add("Confirm Blocker Retracted",
                                           ["Extend Blocker"], 10)     # TODO adjust timer
            return ["Retract Blocker"]
        elif not self.__protocol_handler.can_pickup():
            # We are not allowed to pick up a disk
            self.__expectation_handler.add("Confirm Blocker Retracted",
                                           ["Extend Blocker"], 10)     # TODO adjust timer
            return ["Retract Blocker"]
        else:
            # We want the color and we are allowed to pick up a disk
            self.__expectation_handler.add("Confirm Pusher Push", [], 10)                          # TODO adjust timer
            self.__expectation_handler.add("Secondary Color Detected " + str(color), [], 10)     # TODO adjust timer
            # Inform protocol that we are about to pickup a disk
            self.__protocol_handler.inform_pickup()
            self.__protocol_handler.inform_color(color)
            return ["Push Pusher"]

    def __secondary_color_detected(self, color):
        """
        Removes expectation and returns output in case of secondary color detected.
        @param color  The color that was detected.
        """

        # Remove expectation. If secondary color != primary color,
        # this expectation will not be present and thus an error will be thrown
        self.__expectation_handler.remove("Secondary Color Detected " + str(color))
        # No error thrown, so string disk
        self.__expectation_handler.remove("Confirm Stringer Push", [], 10)                         # TODO adjust timer
        return ["Push Stringer"]

    def __blocker_extended(self):
        """
        Removes expectation and returns output in case of blocker extended.
        """

        self.__expectation_handler.remove("Confirm Blocker Extended")
        self.__expectation_handler.add("Primary Color Detected", [], 10)   # TODO adjust timer
        return ["Scan Color"]

    def __blocker_retracted(self):
        """
        Removes expectation in case of blocker retracted.
        """

        self.__expectation_handler.remove("Confirm Blocker Retracted")

    def __pusher_pushed(self):
        """
        Removes expectation and returns output in case of pusher pushed.
        """

        self.__expectation_handler.remove("Confirm Pusher Push")
        self.__expectation_handler.add("Confirm Blocker Retracted", ["Extend Blocker"], 10)   # TODO adjust timer
        self.__expectation_handler.add("Secondary Color Detected", [], 10)                     # TODO adjust timer
        return ["Retract Blocker"]

    def __disk_stringed(self):
        """
        Removes expectation in case of disk stringed.
        """

        self.__expectation_handler.remove("Confirm Stringer Push")
