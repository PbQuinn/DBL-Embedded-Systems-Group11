class Processor:
    """Processes received messages for the communicator."""

    __stringer = None
    """Stringer to track string status."""

    __protocol_handler = None
    """Protocol handler to communicate with protocol."""

    def __init__(self, protocol_handler):
        pass

    def process(self, msg):
        """Returns message after processing passed message.
        @param msg  The msg to be processed
        """

        pass

    def set_stringer(self, stringer):
        """Set the stringer for processor object."""

        pass
