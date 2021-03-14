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
    __to_bin(int) : void
        creates an array containing the binary representation of the input int
    get_next_color() : int
        returns what color the next disk to be stringed should be
    string_disk(int) : bool
        adds disk to stringed disks, returns if true stringed disk was
        correct color and false otherwise
    is_complete() : bool
        returns whether at least one iteration has been completed
    should_pickup(int) : bool
        returns whether the input color matches the next disk in the pattern
    """

    def __init__(self, goal_int):
        """creates a new instance of Stringer with a goal_int

        @param goal_int  integer whose binary representation will be stringed
        @pre {@code 0 <= goal_int <= 255}
        @raises ValueError  if {@code goal_int < 0 or goal_int > 255}
        """

        if goal_int < 0 or goal_int > 255:
            raise ValueError("Input number should be at least 0,"
                             " and at most 255.")
        self.pattern = self.__to_bin(goal_int)
        self.stringed_disks = []

    def __to_bin(self, goal_int):
        """returns an array of length 8,
        containing the binary representation goal_int

        @pre @code{0 <= goal_int <= 255}
        @post @code{(sum i; 0 <= i < 8; A) == old(goal_int) and goal_bin}
            where @code{A = goal_bin[i]*2**(7 - i)}
        """

        goal_bin = []
        # Convert to binary
        while goal_int > 0:
            if goal_int % 2 == 1:
                goal_bin.insert(0, 1)
                goal_int = goal_int // 2
            else:
                goal_bin.insert(0, 0)
                goal_int = goal_int // 2
        # Add required leading 0s
        while len(goal_bin) < 8:
            goal_bin.insert(0, 0)

        return goal_bin

    def get_next_color(self):
        """returns what color the next disk to be stringed should be

        @pre @code{len(self.pattern) > 0 and not self.is_complete()}
        @post @code{result == self.pattern[A]}
            where @code{A = len(self.stringed_disks) % len(self.pattern)}
        """

        if self.is_complete():
            raise Exception("No next color, Stringer is complete")
        pattern_index = len(self.pattern) - 1 - len(self.stringed_disks)
        disk_color = self.pattern[pattern_index]
        return disk_color

    def string_disk(self, color):
        """adds disk to stringed disks, returns if true stringed disk was
        correct color and false otherwise

        @param color  color of the disk that will be stringed
        @pre @code{color == 1 or color == 0 and not self.is_complete()}
        @modifies self.stringed_disks
        @raises Exception  if @code{self.is_complete()}
        @post @code{(forall i; 0 <= i < old(len(stringed_disks)); A)
            and stringed_disks[0] == color
            and result == (color == self.next_disk())}
            where @code{A = stringed_disks[i+1] == old(stringed_disks[i])}
        """

        if self.is_complete():
            raise Exception("No disk can be stringed, "
                            "since Stringer is complete")
        correct_color = self.get_next_color()
        self.stringed_disks.insert(0, color)
        return color == correct_color

    def is_complete(self):
        """returns whether the pattern has been completely stringed

        @post @code{result == (len(self.stringed_disks)
                              // len(self.pattern) > 0)}
        """

        return len(self.stringed_disks) // len(self.pattern) > 0

    def should_pickup(self, color):
        """returns whether the input color matches the next disk in the pattern

        @param color  color of the disk that will be stringed
        @pre @code{color == 1 or color == 0}
        @post @code{result == (color == get_next_color())}
        """

        return color == self.get_next_color()
