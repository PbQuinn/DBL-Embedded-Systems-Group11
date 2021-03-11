from disk_string import Stringer
from protocol_handler import ProtocolHandler
from talk_to_push import ArduinoDiskPusher


# The main class that will be setup and then will run all interactions
class Main:
    """The main class consisting of a setup and a main loop

    Attributes
    __________
    string : DiskString
        a string object containing information on the already stringed disks
    goal_int : int
        the integer that will be represented in binary using the stringed disks

    Methods
    _______
    run() : void
        runs setup and main loop of Stringer instance
    """

    def __init__(self, goal_int, disk_pusher=ArduinoDiskPusher()):
        """
        Creates a new instance of Stringer with goalInt as goal integer

        @param goal_int  the integer that this stringer will string
        @pre @code{goalInt >= 0}
        """

        if goal_int < 0:
            raise ValueError("goalInt should be positive")
        self.goal_int = goal_int
        self.string = Stringer(goal_int)
        self.disk_counter = 0
        self.protocol = ProtocolHandler()
        self.pusher = disk_pusher

    def run(self):
        """Runs the main loop of the program

        """
        # TODO improve / modify main loop
        # Main loop:
        while True:
            self.pusher.pulse()
            data = self.pusher.get_data()
            if (data is not None) and self.protocol.get_permission():
                self.pusher.close_gate()
                color = self.pusher.get_color()
                if color == self.string.get_next_disk():
                    self.pusher.push_disk()
                    self.string.string_disk(color)
                self.pusher.open_gate()


if __name__ == '__main__':
    valid_integer = False
    while not valid_integer:
        try:
            number = int(input('Enter a positive integer to use:'))
            my_stringer = Main(number)
            valid_integer = True
            print('We will use ' + str(number))
        except ValueError:
            print('The number should be an integer >= 0')

