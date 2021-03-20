class Processor:
    """
    Processes input and returns output for the communicator.

    Attributes
    __________
    __string_handler : StringHandler
        An instance of a string handler to track the string status

    __protocol_handler : ProtocolHandler
        An instance of the protocol handler to communicate with protocol

    __expectation_handler : ExpectationHandler
        An instance of the expectation handler to track expected inputs

    __ping_counter : int
        The number of pings since protocol was last informed of our existence

    __PROTOCOL_PING_FREQUENCY : int
        The interval in pings at which the protocol will be notified
        of our existence

    __is_stringing : int
        Keeps track of whether we are currently stringing a disk

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

    def __init__(self, string_handler, protocol_handler, expectation_handler):
        self.__string_handler = string_handler
        self.__protocol_handler = protocol_handler
        self.__expectation_handler = expectation_handler
        self.__ping_counter = 0
        self.__is_stringing = False

    def process(self, input_):
        """
        After processing input and output, returns output.
        @param input_  The input to be processed
        """

        output = self.__process_input(input_)
        self.__process_output(input_, output)
        return output

    def __process_input(self, input_):
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
            elif input_ == "Tertiary Motion":
                return self.__tertiary_motion()
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
            print(error)
            return ["Error Occurred"]

    def __process_output(self, input_, outputs):
        """
        Processes output, i.e. adds expectations for each output.
        @param input_  The input
        @param outputs  List of outputs to be processed
        """

        for output in outputs:
            if output == "Extend Blocker":
                self.__expectation_handler.add("Confirm Blocker Extended", ["Retract Blocker"], 10,  # TODO adjust timer
                                               "We did not receive confirmation for blocker retracting. Please make " +
                                               "sure the blocker is not obstructed by any objects and that its " +
                                               "sensors are in order.")
            elif output == "Retract Blocker":
                self.__expectation_handler.add("Confirm Blocker Retracted", ["Extend Blocker"], 10,  # TODO adjust timer
                                               "We did not receive confirmation for blocker extending. Please make " +
                                               "sure the blocker is not obstructed by any objects and that its " +
                                               "sensors are in order.")
            elif output == "Push Pusher":
                self.__expectation_handler.add("Confirm Pusher Pushed", ["Ignore"], 10,  # TODO adjust timer
                                               "We did not receive confirmation for pusher pushing. Please make " +
                                               "sure the pusher is not obstructed by any objects and that its " +
                                               "sensors are in order.")
                if input_ == "Primary White":
                    self.__expectation_handler.add("Secondary White Detected", ["Ignore"], 10,  # TODO adjust timer
                                                   "We pushed a white disk into the funnel, but it was not detected " +
                                                   "by the secondary color sensor. Please check whether the funnel " +
                                                   "is in order. If there is a black disk in the funnel, please " +
                                                   "remove it. Otherwise, please check whether the sensors are in " +
                                                   "order.")
                    self.__expectation_handler.add("Secondary Motion", ["Ignore"], 10,  # TODO adjust timer
                                                   "We pushed a white disk into the funnel, but it was not detected " +
                                                   "by the secondary motion sensor. Please check whether the funnel " +
                                                   "is in order. If something is blocking the funnel, please remove" +
                                                   " it. Otherwise, please check whether the sensors are in order.")
                elif input_ == "Primary Black":
                    self.__expectation_handler.add("Secondary Black Detected", ["Ignore"], 10,  # TODO adjust timer
                                                   "We pushed a black disk into the funnel, but it was not detected " +
                                                   "by the secondary color sensor. Please check whether the funnel " +
                                                   "is in order. If there is a white disk in the funnel, please " +
                                                   "remove it. Otherwise, please check whether the sensors are in " +
                                                   "order.")
                    self.__expectation_handler.add("Secondary Motion", ["Ignore"], 10,  # TODO adjust timer
                                                   "We pushed a black disk into the funnel, but it was not detected " +
                                                   "by the secondary motion sensor. Please check whether the funnel " +
                                                   "is in order. If something is blocking the funnel, please remove" +
                                                   " it. Otherwise, please check whether the sensors are in order.")
            elif output == "Push Stringer":
                self.__expectation_handler.add("Tertiary Motion", ["Ignore"], 10,  # TODO adjust timer
                                               "We asked the stringer to push, but we did not receive confirmation " +
                                               "from the tertiary motion sensor. Please check whether the stringer " +
                                               "is in order.")

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

        if not self.__string_handler.is_complete() and not self.__is_stringing:
            # The stringer still needs disks
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

    def __tertiary_motion(self):
        """
        Removes expectation in case of tertiary motion.
        """

        self.__is_stringing = False
        self.__expectation_handler.remove("Tertiary Motion")
        return ["Ignore"]

    def __primary_color_detected(self, color):
        """
        Removes expectation and returns output in case of color.
        @param color  The color that was detected.
        """

        self.__expectation_handler.remove("Primary Color Detected")

        if not self.__string_handler.should_pickup(color):
            # We do not want the color
            print('\033[93m' + "Stringer: we should not pick up this disk." + '\033[0m')
            return ["Retract Blocker"]
        elif not self.__protocol_handler.can_pickup():
            # We are not allowed to pick up a disk
            print('\033[93m' + "Protocol: we are not allowed to pick up this disk." + '\033[0m')
            return ["Retract Blocker"]
        else:
            # We want the color and we are allowed to pick up a disk
            print('\033[93m' + "Stringer and protocol: we should and are allowed to pick up this disk." + '\033[0m')
            # Inform protocol that we are about to pick up a disk
            self.__protocol_handler.inform_pickup()
            self.__protocol_handler.inform_color(color)
            # Update Stringer
            self.__string_handler.string_disk(color)
            return ["Push Pusher"]

    def __secondary_color_detected(self, color):
        """
        Removes expectation and returns output in case of secondary color
        detected.
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
        return ["Push Stringer"]

    def __blocker_extended(self):
        """
        Removes expectation and returns output in case of blocker extended.
        """

        self.__expectation_handler.remove("Confirm Blocker Extended")
        return ["Scan Primary Color"]

    def __blocker_retracted(self):
        """
        Removes expectation in case of blocker retracted.
        """

        self.__expectation_handler.remove("Confirm Blocker Retracted")
        return ["Ignore"]

    def __pusher_pushed(self):
        """
        Removes expectation and returns output in case of pusher pushed.
        """

        self.__is_stringing = True
        self.__expectation_handler.remove("Confirm Pusher Pushed")
        return ["Retract Blocker"]
