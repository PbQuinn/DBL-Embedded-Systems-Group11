class Processor:
    """Processes received messages for the communicator."""

    __protocol_handler = None
    """Protocol handler to communicate with protocol."""

    __stringer = None
    """Stringer to track string status."""

    def __init__(self, protocol_handler):
        self.__protocol_handler = protocol_handler

    def set_stringer(self, stringer):
        """
        Sets the stringer for this processor object.
        @param stringer  Stringer to be set
        """

        self.__stringer = stringer

    def process(self, msg):
        """
        Returns message after processing passed message.
        @param msg  The msg to be processed
        """

        if msg == b"Ping":
            return [b"Pong"]
        elif msg == b"Motion":
            return self.__motion()
        elif msg == [b"White"]:
            return self.__color(0)
        elif msg == [b"Black"]:
            return self.__color(1)
        else:
            return [b"Unknown Message"]

    def __motion(self):
        """Returns command in case of motion."""

        if not self.__stringer.complete():
            # The stringer still needs disks
            return [b"Extend Blocker", b"Scan Color"]
        else:
            # The stringer does not need disks
            return [b"Ignore"]

    def __color(self, color):
        """
        Returns command in case of color.
        @param color  The color that was detected.
        """

        if not self.__stringer.should_pickup(color):
            # We do not want the color
            return [b"Retract Blocker"]
        elif not self.__protocol_handler.can_pickup():
            # We are not allowed to pick up a disk
            return [b"Retract Blocker"]
        else:
            # We want the color and we are allowed to pick up a disk
            return [b"Push", b"Retract Blocker"]
