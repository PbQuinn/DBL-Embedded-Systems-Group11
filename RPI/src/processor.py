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

    __ping_counter : int
        The number of pings since protocol was last informed of our existence

    __PROTOCOL_PING_FREQUENCY : int
        The interval in pings at which the protocol will be notified
        of our existence

    Methods
    _______
    process(string) : string[*]
        Takes input, processes it, and returns output

    __ping() : string[*]
        Upon corresponding input, pings expectation handler and returns output

    __primary_motion() : string[*]
        Upon corresponding input, returns output

    __secondary_motion() : string[*]
        Upon corresponding input, returns output

    __primary_color_detected(int) : string[*]
        Upon corresponding input, returns output

    __primary_color_detected(int) : string[*]
        Upon corresponding input, returns output

    __blocker_extended()
        Upon corresponding input, returns output

    __blocker_retracted()
        Upon corresponding input, returns output

    __pusher_pushed()
        Upon corresponding input, returns output

    __tertiary_motion()
        Upon corresponding input, returns output
    """

    # The protocol will be notified of our existence every
    # PROTOCOL_PING_FREQUENCY th ping
    __PROTOCOL_PING_FREQUENCY = 10

    def __init__(self, stringer, protocol_handler, expectation_handler):
        self.__stringer = stringer
        self.__protocol_handler = protocol_handler
        self.__expectation_handler = expectation_handler
        self.__ping_counter = 0

    def process(self, input_):
        """
        Returns output after processing passed input.
        @param input_  The input to be processed
        """

        try:
            # Main interactions:
            if input_ == "Ping":
                return self.__ping()
            elif input_ == "Primary Motion":
                return self.__primary_motion()
            elif input_ == "Secondary Motion":
                return self.__secondary_motion()
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
            elif input_ == "Confirm Pusher Pushed":
                return self.__pusher_pushed()
            elif input_ == "Tertiary Motion":
                return self.__tertiary_motion()

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
        except ValueError as error:
            return ["Error Occurred", error]

    def __ping(self):
        """
        Returns output in case of ping.
        """

        self.__expectation_handler.ping()
        self.__ping_counter += 1
        if self.__ping_counter % self.__PROTOCOL_PING_FREQUENCY == 0:
            self.__protocol_handler.inform_alive()
            self.__ping_counter = 0
        expired_outputs = self.__expectation_handler.get_expired_outputs()
        return ["Pong"] + expired_outputs

    def __primary_motion(self):
        """
        Returns output in case of primary motion.
        """

        if not self.__stringer.is_complete():
            # The stringer still needs disks
            self.__expectation_handler.add("Confirm Blocker Extended",
                                           ["Retract Blocker"], 10)    # TODO adjust timer
            return ["Extend Blocker"]
        else:
            # The stringer does not need disks
            return ["Ignore"]

    def __secondary_motion(self):
        """
        Removes expectation and returns output in case of secondary motion
        """

        self.__expectation_handler.remove("Secondary Motion")
        return ["Scan Secondary Color"]

    def __primary_color_detected(self, color):
        """
        Removes expectation and returns output in case of color.
        @param color  The color that was detected.
        """

        self.__expectation_handler.remove("Primary Color Detected")

        if not self.__stringer.should_pickup(color):
            # We do not want the color
            self.__expectation_handler.add("Confirm Blocker Retracted",
                                           ["Extend Blocker"], 10)              # TODO adjust timer
            return ["Retract Blocker"]
        elif not self.__protocol_handler.can_pickup():
            # We are not allowed to pick up a disk
            self.__expectation_handler.add("Confirm Blocker Retracted",
                                           ["Extend Blocker"], 10)              # TODO adjust timer
            return ["Retract Blocker"]
        else:
            # We want the color and we are allowed to pick up a disk
            if color == 1:
                color_name = "Black"
            else:
                color_name = "White"
            # Add expectation for secondary color, including color name
            self.__expectation_handler.add("Secondary " + color_name +
                                           " Detected", [], 10)                 # TODO adjust timer
            self.__expectation_handler.add("Secondary Motion", [], 10)          # TODO adjust timer
            # Inform protocol that we are about to pickup a disk
            self.__protocol_handler.inform_pickup()
            self.__protocol_handler.inform_color(color)

            self.__expectation_handler.add("Confirm Pusher Pushed", [], 10)  # TODO adjust timer
            return ["Push Pusher"]

    def __secondary_color_detected(self, color):
        """
        Removes expectation and returns output in case of secondary color detected.
        @param color  The color that was detected.
        """

        # Remove expectation. If secondary color != primary color,
        # this expectation will not be present and thus an error will be thrown
        if color == 1:
            color_name = "Black"
        else:
            color_name = "White"
        self.__expectation_handler.remove("Secondary " + color_name +
                                          " Detected")
        # No error thrown, so string disk
        self.__expectation_handler.add("Confirm Tertiary Motion", [], 10)    # TODO adjust timer
        return ["Push Stringer"]

    def __blocker_extended(self):
        """
        Removes expectation and returns output in case of blocker extended.
        """

        self.__expectation_handler.remove("Confirm Blocker Extended")
        self.__expectation_handler.add("Primary Color Detected", [], 10)   # TODO adjust timer
        return ["Scan Primary Color"]

    def __blocker_retracted(self):
        """
        Removes expectation in case of blocker retracted.
        """

        self.__expectation_handler.remove("Confirm Blocker Retracted")

    def __pusher_pushed(self):
        """
        Removes expectation and returns output in case of pusher pushed.
        """

        self.__expectation_handler.remove("Confirm Pusher Pushed")
        self.__expectation_handler.add("Confirm Blocker Retracted",
                                       ["Extend Blocker"], 10)              # TODO adjust timer
        return ["Retract Blocker"]

    def __tertiary_motion(self):
        """
        Removes expectation in case of tertiary motion.
        """

        self.__expectation_handler.remove("Confirm Tertiary Motion")
