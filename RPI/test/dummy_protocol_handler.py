class DummyProtocolHandler:
    """Class used for imitating ProtocolHandler

        Attributes
        __________
        allowance : bool
            the token used for authorization when communicating with the
            protocol, obtained upon initialization

        Methods
        _______
        set_allowance(bool) : void
            Changes the allowance to the given boolean
        can_pickup() : bool
            Returns true iff next disk may be retrieved
        """

    def __init__(self, allowance):
        self.allowance = allowance

    def set_allowance(self, allowance):
        """Changes the allowance to the given boolean
        """
        self.allowance = allowance

    def can_pickup(self):
        """Returns true iff next disk may be retrieved
        """
        return self.allowance

    def inform_pickup(self):
        return

    def inform_color(self, color):
        return
