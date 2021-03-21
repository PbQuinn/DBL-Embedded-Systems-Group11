class Expectation:
    """
    Processes input and returns output for the communicator.

    Attributes
    __________
    __input : string
        The expected input

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

    get_msg() : string
        Returns the msg attribute

    has_expired() : bool
        Returns whether this expectation has expired
    """

    def __init__(self, input_, pings, msg):
        self.__input_ = input_
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

        return self.__input_

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
