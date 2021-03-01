from disk_string import DiskString

# The main class that will be setup and then will run all interactions
class Stringer:
    """The main class consisting of a setup and a main loop

    Attributes
    __________
    string : DiskString
        a string object containing information on the already stringed disks
    goal_int : int
        the integer that will be represented in binary using the stringed disks

    Methods
    _______
    to_bin() : void
        creates an array containing the binary representation of self.goal_int
        and assigns it to self.goal_bin

    run() : void
        runs setup and main loop of Stringer instance
    """

    def __init__(self, goalInt):
        """
        Creates a new instance of Stringer with goalInt as goal integer

        @param goalInt  the integer that this stringer will string
        @pre @code{goalInt >= 0}
        """
        if goalInt < 0:
            raise ValueError("goalInt should be positive")
        self.goal_int = goalInt
        self.goal_bin = []
        self.to_bin()
        self.string = DiskString(self.goal_bin)

    def to_bin(self):
        """ creates an array containing the binary representation of
        self.goal_int and assigns it to self.goal_bin

        @pre @code{self.goalInt >= 0}
        @modifies self.goalBin
        @post @code{(sum i; 0 <= i < len(goalBin); A) == self.goalInt}
            where @code{A = a[i]*2**(len(goalBin) - 1 - i)}
        """
        goal = self.goal_int
        if goal == 0:
            goal_bin = [0]
        else:
            while goal > 0:
                if goal % 2 == 1:
                    self.goal_bin.insert(0, 1)
                    goal = goal // 2
                    print(goal)
                else:
                    self.goal_bin.insert(0, 0)
                    goal = goal // 2
                    print(goal)

    def run(self):
        """

        """
        return

if __name__ == '__main__':
    valid_integer = False
    while not valid_integer:
        try:
            number = int(input('Enter a positive integer to use:'))
            my_stringer = Stringer(number)
            valid_integer = True
            print('We will use ' + str(number))
        except ValueError:
            print('The number should be an integer >= 0')

    # Test line
    print(my_stringer.goal_bin)



