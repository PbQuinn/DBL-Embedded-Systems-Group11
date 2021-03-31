from enum import Enum


class Color(Enum):
    Black = 1
    White = 0
    Neither = -1


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

    __current_color : Color
        Keeps track of which color we are currently stringing

    __error_mode: bool
        Indicates whether the to_string() system is in error mode

    Methods
    _______
    flush() : void
        Flushes expectation handler and sets current color to neither

    process(string) : string[*]
        Takes input, processes it, and returns output

    get_error_mode() : bool
        Returns whether the processor is in error mode

    set_error_mode(bool) : void
        Sets the error mode

    __process_input(string) : string[*]
        Returns output after processing passed input

    __process_output(string) : void
        Processes output, i.e. adds expectations for each output.

    __ping() : string[1]
        Upon corresponding input, pings expectation handler and returns output

    __primary_motion() : string[1]
        Upon corresponding input, returns output

    __secondary_motion() : string[1]
        Upon corresponding input, returns output

    __tertiary_motion() : string[1]
        Upon corresponding input, returns output

    __primary_color_detected(int) : string[1]
        Upon corresponding input, returns output

    __secondary_color_detected(int) : string[1]
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
        self.__current_color = Color.Neither
        self.__error_mode = False

    def flush(self):
        """
        Flushes expectation handler and set current color to neither
        """
        self.__expectation_handler.flush()
        self.__current_color = Color.Neither

    def process(self, input_):
        """
        After processing input and output, returns output.
        @param input_  The input to be processed
        """

        output = self.__process_input(input_)
        self.__process_output(output)
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
                return self.__primary_color_detected(Color.White)
            elif input_ == "Primary Black":
                return self.__primary_color_detected(Color.Black)
            elif input_ == "Primary Neither":
                return self.__primary_color_detected(Color.Neither)
            elif input_ == "Secondary White":
                return self.__secondary_color_detected(Color.White)
            elif input_ == "Secondary Black":
                return self.__secondary_color_detected(Color.Black)
            elif input_ == "Confirm Blocker Extended":
                self.__expectation_handler.remove("Confirm Blocker Extended",
                                                  "We received Confirm Blocker Extended input,"
                                                  " but we did not expect it.")
                return ["Scan Primary Color"]
            elif input_ == "Confirm Blocker Retracted":
                self.__expectation_handler.remove("Confirm Blocker Retracted",
                                                  "We received Confirm Blocker Retracted input,"
                                                  " but we did not expect it.")
                return ["Ignore"]
            elif input_ == "Confirm Pusher Pushed":
                self.__expectation_handler.remove("Confirm Pusher Pushed",
                                                  "We received Confirm Pusher Pushed input,"
                                                  " but we did not expect it.")
                return ["Retract Blocker"]
            elif input_ == "Error Ping":
                if not self.__error_mode:
                    raise ValueError('\033[91m' +
                                     "The Arduino sent a signal indicating that it has entered error mode."
                                     "The RPI was not expecting this." + '\033[0m')
            elif input_ == "Error Mode Exited":
                return ["Ignore"]
            # Error interactions:
            elif input_ == "Secondary Neither":
                raise ValueError('\033[91m' +
                                 "The secondary color sensor detected a color that was"
                                 " not recognized as black nor white.\n"
                                 "Please ensure that there is no external light source"
                                 " interfering with the sensor,\n"
                                 "that there are only black and white disks in the"
                                 " funnel,\n"
                                 "and that the secondary color sensor is in order."
                                 + '\033[0m')
            elif input_ == "Error String Disk":
                raise ValueError('\033[91m' + "Something went wrong while stringing the"
                                              " disk. Please check whether the stringer"
                                              " and string are in order." + '\033[0m')
            elif input_ == "Unexpected Error Occurred":
                raise ValueError('\033[91m' + "An unexpected error occurred within the"
                                              " Arduino code." + '\033[0m')
            elif input_ == "Illegal Command Sent":
                raise ValueError('\033[91m' + "The Arduino received a known but"
                                              " unexpected command from the RPI."
                                 + '\033[0m')
            elif input_ == "Unknown Command Sent":
                raise ValueError('\033[91m' + "The Arduino received an unknown command"
                                              " from the RPI. Please check whether the"
                                              " connection between the two is in order."
                                 + '\033[0m')
            elif input_ == "Message Buffer Full":
                raise ValueError('\033[91m' + "The message buffer of the Arduino is"
                                              " full. Please check whether the"
                                              " connection between the two is in order."
                                 + '\033[0m')
            else:
                raise ValueError('\033[91m' + "Unknown message received:"
                                              " %s" % input_ + '\033[0m')
        except ValueError as error:
            print('\033[91m' + "An error has occurred:" + '\033[0m')
            print(error)
            self.set_error_mode(True)
            return ["Enter Error Mode"]

    def __process_output(self, outputs):
        """
        Processes output, i.e. adds expectations for each output.
        @param outputs  List of outputs to be processed
        """

        for output in outputs:
            if output == "Extend Blocker":
                self.__expectation_handler.add("Confirm Blocker Extended", 5,  # TODO adjust timer
                                               "We did not receive confirmation for blocker retracting.\n" +
                                               "Please make sure the blocker is not obstructed by any objects and " +
                                               "that its sensors are in order.")
            elif output == "Retract Blocker":
                self.__expectation_handler.add("Confirm Blocker Retracted", 5,  # TODO adjust timer
                                               "We did not receive confirmation for blocker extending.\n" +
                                               " Please make  sure the blocker is not obstructed by any objects and " +
                                               "that its sensors are in order.")
            elif output == "Push Pusher":
                self.__expectation_handler.add("Confirm Pusher Pushed", 10,  # TODO adjust timer
                                               "We did not receive confirmation for pusher pushing.\n" +
                                               "Please make sure the pusher is not obstructed by any objects and "
                                               "that its sensors are in order.")
                self.__expectation_handler.add("Secondary Motion", 10,  # TODO adjust timer
                                               "We attempted to push a disk into the funnel, but it has not been " +
                                               "detected by the secondary motion sensor.\n" +
                                               "Please check whether the pusher and the funnel are in order.\n" +
                                               "If something is blocking either of them, please fix it.\n" +
                                               "Otherwise, please check whether the secondary motion sensor is " +
                                               "in order.")
            elif output == "Push Stringer":
                self.__expectation_handler.add("Tertiary Motion", 5,  # TODO adjust timer
                                               "We asked the stringer to push, but we did not receive confirmation " +
                                               "from the tertiary motion sensor.\n" +
                                               " Please check whether the stringer is in order.")
            elif output == "Scan Primary Color":
                self.__expectation_handler.add("Primary Color Detected", 3,  # TODO adjust timer
                                               "We asked the primary color sensor to scan a color, but we did not " +
                                               "receive it.\n" +
                                               "Please check whether the primary color sensor is in order.")
            elif output == "Scan Secondary Color":
                if self.__current_color == Color.White:
                    self.__expectation_handler.add("Secondary White Detected", 3,  # TODO adjust timer
                                                   "We pushed a white disk into the funnel, but it was not detected " +
                                                   "by the secondary color sensor.\n" +
                                                   "Please check whether the funnel is in order.\n" +
                                                   "If there is a black disk in the funnel, please remove it.\n" +
                                                   "Otherwise, please check whether the sensors are in order.")
                elif self.__current_color == Color.Black:
                    self.__expectation_handler.add("Secondary Black Detected", 3,  # TODO adjust timer
                                                   "We pushed a black disk into the funnel, but it was not detected " +
                                                   "by the secondary color sensor.\n" +
                                                   "Please check whether the funnel is in order.\n" +
                                                   "If there is a white disk in the funnel, please remove it.\n" +
                                                   "Otherwise, please check whether the sensors are in order.")

    def __ping(self):
        """
        Returns output in case of ping.
        """

        self.__ping_counter += 1

        if self.__ping_counter % self.__PROTOCOL_PING_FREQUENCY == 0:
            self.__protocol_handler.inform_alive()
            self.__ping_counter = 0

        self.__expectation_handler.ping()

        return ["Pong"]

    def __primary_motion(self):
        """
        Returns output in case of primary motion.
        """

        if not self.__string_handler.is_complete() and self.__current_color == Color.Neither:
            # The stringer still needs disks
            return ["Extend Blocker"]
        else:
            # The stringer does not need disks
            return ["Ignore"]

    def __secondary_motion(self):
        """
        Removes expectation and returns output in case of secondary motion
        """

        self.__expectation_handler.remove("Secondary Motion",
                                          "We received secondary motion, but did not expect it.\n" +
                                          "Please, remove any objects from the secondary motion sensor\n" +
                                          "If there are no objects there, please make sure the sensor is OK.")
        return ["Scan Secondary Color"]

    def __tertiary_motion(self):
        """
        Removes expectation in case of tertiary motion.
        """

        # No error thrown, so string disk
        self.__string_handler.string_disk(self.__current_color.value)
        self.__current_color = Color.Neither
        self.__expectation_handler.remove("Tertiary Motion",
                                          "We received Tertiary Motion input, but did not expect it.\n" +
                                          "Please, remove any objects from the tertiary motion sensor\n" +
                                          "If there are no objects there, please make sure the sensor is OK.")
        return ["Ignore"]

    def __primary_color_detected(self, color):
        """
        Removes expectation and returns output in case of color.
        @param color  The color that was detected.
        """

        self.__expectation_handler.remove("Primary Color Detected",
                                          "We received Primary Color Detected input, but we did not expect it.")

        if not self.__string_handler.should_pickup(color.value):
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
            self.__protocol_handler.inform_color(color.value)
            # Update current color
            self.__current_color = color
            return ["Push Pusher"]

    def __secondary_color_detected(self, color):
        """
        Removes expectation and returns output in case of secondary color
        detected.
        @param color  The color that was detected.
        """

        # Remove expectation. If secondary color != primary color,
        # this expectation will not be present and thus an error will be thrown
        self.__expectation_handler.remove("Secondary " + str(color.name) + " Detected",
                                          "We received Secondary Color Detected input for " + str(color.name) +
                                          ", but we were expecting " + str(self.__current_color.name) + ".\n" +
                                          "Please, check up on the secondary color sensor and remove any objects.")
        return ["Push Stringer"]

    def get_error_mode(self):
        """
        Returns whether the processor is in error mode.
        """

        return self.__error_mode

    def set_error_mode(self, error_mode):
        """
        Sets the error mode.
        """

        self.__error_mode = error_mode
