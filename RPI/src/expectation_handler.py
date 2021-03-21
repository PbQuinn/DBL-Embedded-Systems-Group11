from RPI.src.expectation import Expectation


class ExpectationHandler:
    """
    Processes input and returns output for the communicator.

    Attributes
    __________
    __expectations : Expectation[*]
        The current expectations for input

    Methods
    _______
    ping() : void
        Pings each expectation

    add(string, int, string) : void
        Creates and adds expectation with passed arguments

    remove() : void
        Upon corresponding input, returns output

    get_expired_outputs() : string[*]
        Upon corresponding input, returns output

    flush() : void
        Remove all expectations
    """

    def __init__(self):
        self.__expectations = []

    def ping(self):
        """
        Pings each expectation
        """

        for expectation in self.__expectations:
            expectation.ping()

        self.__check_expiration()

    def flush(self):
        """
        Removes all expectations
        """

        self.__expectations = []

    def add(self, input_, pings, msg):
        """
        Creates and adds expectation with passed arguments
        @param input_  The input that is expected
        @param output  The output that should be returned upon expiration
        @param  pings  The number of pings until the expectation expires
        @param  msg  The msg that will be printed when expectation expires
        """

        # Create new expectation and add it to the front of the list
        expectation = Expectation(input_, pings, msg)
        self.__expectations.insert(0, expectation)
        print('\033[92m' + "Added expectation: " + input_ + '\033[0m')

    def remove(self, input_, msg):
        """
        Removes last expectation that matches with input or raises error when there is no such expectation
        @param input_  The input of the expectation that should be removed
        @param msg  The message in case of error
        """

        # Take the matching expectations
        matching_expectations = [e for e in self.__expectations if input_ == e.get_input()]

        # Take the other expectations
        other_expectations = [e for e in self.__expectations if input_ != e.get_input()]

        if matching_expectations:
            # Remove expectation at the end of the matching list
            matching_expectations.pop()

            # Append the matching list with other expectations and update expectation list
            self.__expectations = other_expectations + matching_expectations
            print('\033[92m' + "Removed expectation: " + input_ + '\033[0m')
        else:
            raise ValueError(msg)

    def __check_expiration(self):
        """
        Checks whether there are expired expectations, raises error if so
        """

        # Take expired expectations
        expired_expectations = [e for e in self.__expectations if e.has_expired()]

        # Remove expired expectations from expectations
        self.__expectations = [e for e in self.__expectations if not e.has_expired()]

        if expired_expectations:
            msg = ""

            # Get message for each expired expectation
            for expectation in expired_expectations:
                msg += '\033[91m' + expectation.get_msg() + '\033[0m' + "\n"

            raise ValueError(msg)
