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
    to_bin() : void
        creates an array containing the binary representation of self.goal_int
        and assigns it to self.goal_bin
    get_next_disk() : int
        returns what color the next disk to be stringed should be
    string_disk(int) : bool
        adds disk to stringed disks, returns if true stringed disk was
        correct color and false otherwise
    get_iteration() : int
        returns the number of times the pattern has been completed
    is_complete() : bool
        returns whether at least one iteration has been completed
    """

    def __init__(self, goal_int):
        """creates a new instance of Stringer with a goal_int

        @param goal_int  integer whose binary representation will be stringed
        @pre @code{len(pattern) > 0 and (forall i; 0 <= i < len(pattern); A)}
            where @code{A = pattern[i] == 0 or pattern[i] == 1}
        """
        if goal_int < 0:
            raise ValueError("Input number should be positive")
        self.pattern = self.__to_bin(goal_int)
        self.stringed_disks = []

    def __to_bin(self, goal_int):
        """returns an array containing the binary representation goal_int

        @pre @code{self.goalInt >= 0}
        @modifies self.goalBin
        @post @code{(sum i; 0 <= i < len(goal_bin); A) == old(goal_int)}
            where @code{A = goal_bin[i]*2**(len(goal_bin) - 1 - i)}
        """

        goal_bin = []
        if goal_int == 0:
            goal_bin = [0]
        else:
            while goal_int > 0:
                if goal_int % 2 == 1:
                    goal_bin.insert(0, 1)
                    goal_int = goal_int // 2
                else:
                    goal_bin.insert(0, 0)
                    goal_int = goal_int // 2
        return goal_bin

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

    def is_complete(self):
        """returns whether at least one iteration has been completed

        @post @code{result == get_iteration > 1}
        """

        return self.get_iteration() > 0
