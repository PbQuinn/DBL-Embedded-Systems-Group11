class Stringer:
    """Class representing the string and the disks on it

    Attributes
    __________
    pattern : int[1..*]
        the pattern according to which disks should be added to the string
    stringed_disks : int[*]
        represents the currently stringed disks

    Methods
    _______
    get_next_disk() : int
        returns what color the next disk to be stringed should be
    string_disk(int) : bool
        adds disk to stringed disks, returns if true stringed disk was
        correct color and false otherwise
    get_iteration() : int
        returns the number of times the pattern has been completed
    """

    def __init__(self, pattern):
        """Creates a new instance of DiskString from a pattern array

        @param pattern  an array containing a pattern of ones and zeroes
        @pre @code{len(pattern) > 0 and (forall i; 0 <= i < len(pattern); A)}
            where @code{A = pattern[i] == 0 or pattern[i] == 1}
        """
        if len(pattern) == 0:
            raise ValueError("Pattern should have length of at least 1")
        self.pattern = pattern
        self.stringed_disks = []

    def get_next_disk(self):
        """returns what color the next disk to be stringed should be

        @pre @code{len(self.pattern) > 0}
        @post @code{result == self.pattern[A]}
            where @code{A = len(self.stringed_disks) % len(self.pattern)}
        """

        pattern_index = len(self.pattern) - 1 - \
                        len(self.stringed_disks) % len(self.pattern)
        disk_color = self.pattern[pattern_index]
        return disk_color

    def string_disk(self, color):
        """adds disk to stringed disks, returns if true stringed disk was
        correct color and false otherwise

        @param color  color of the disk that will be stringed
        @pre @code{color == 1 or color == 0}
        @modifies self.stringed_disks
        @post @code{(forall i; 0 <= i < old(len(stringed_disks)); A)
            and stringed_disks[0] == color
            and result == (color == self.next_disk())}
            where @code{A = stringed_disks[i+1] == old(stringed_disks[i])}
        """

        correct_color = self.get_next_disk()
        self.stringed_disks.insert(0, color)
        return color == correct_color

    def get_iteration(self):
        """returns the number of times the pattern has been completed

        @post @code{result == len(self.stringed_disks) // len(self.pattern)}
        """

        return len(self.stringed_disks) // len(self.pattern)
