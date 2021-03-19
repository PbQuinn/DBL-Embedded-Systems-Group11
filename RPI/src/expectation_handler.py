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

    add(string, string[*], int) : void
        Creates and adds expectation with passed arguments

    remove() : void
        Upon corresponding input, returns output

    get_expired_outputs() : string[*]
        Upon corresponding input, returns output
    """

    def __init__(self):
        self.__expectations = []

    def ping(self):
        """
        Pings each expectation
        """

        for expectation in self.__expectations:
            expectation.ping()

    def add(self, input_, output, pings):
        """
        Creates and adds expectation with passed arguments
        @param input_  The input that is expected
        @param output  The output that should be returned upon expiration
        @param  pings  The number of pings until the expectation expires
        """

        # Create new expectation and add it to the front of the list
        expectation = Expectation(input_, output, pings)
        self.__expectations.insert(0, expectation)

    def remove(self, input_):
        """
        Removes last expectation that matches with input
        @param input_  The input of the expectation that should be removed
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
        else:
            raise ValueError("Unexpected input: " + input_)

    def get_expired_outputs(self):
        """
        Removes expired expectations and returns their output values
        """

        # Take expired expectations
        expired_expectations = [e for e in self.__expectations if e.has_expired()]

        # Remove expired expectations from expectations
        self.__expectations = [e for e in self.__expectations if not e.has_expired()]

        expired_outputs = []

        # Get output of each expired expectation
        for expectation in expired_expectations:
            expired_outputs += expectation.get_output()

        return expired_outputs
