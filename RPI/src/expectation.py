class Expectation:
    """
    Processes input and returns output for the communicator.

    Attributes
    __________
    __input : string
        The expected input

    __output : string[*]
        The output in case of expiration

    __pings : int
        The number of pings until expiration

    Methods
    _______
    ping() : void
        Pings each expectation

    get_input() : string
        Returns the input attribute

    get_output() : string[*]
        Returns the output attribute

    has_expired() : bool
        Returns whether this expectation has expired
    """

    def __init__(self, input, output, pings):
        self.__input = input
        self.__output = output
        self.__pings = pings

    def ping(self):
        """
        Decrements pings attribute and reports upon expiration
        """

        self.__pings -= 1

        if self.has_expired():
            input_string = self.__input.decode("utf-8")
            output_string = b''.join(self.__output).decode("utf-8")
            print("Expectation for input " + input_string + " has expired, " + output_string + " will be output.")

    def get_input(self):
        """
        Returns input attribute
        """

        return self.__input

    def get_output(self):
        """
        Returns output attribute
        """

        return self.__output

    def has_expired(self):
        """
        Returns whether this expectation has expired
        """

        return self.__pings < 1
