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

    __msg : string
        The message in case of expiration

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

    def __init__(self, input_, output, pings, msg):
        self.__input = input_
        self.__output = output
        self.__pings = pings
        self.__msg = msg

    def ping(self):
        """
        Decrements pings attribute and reports upon expiration
        """

        self.__pings -= 1

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

    def get_msg(self):
        """
        Returns msg attribute
        """

        return self.__msg

    def has_expired(self):
        """
        Returns whether this expectation has expired
        """

        return self.__pings < 1
