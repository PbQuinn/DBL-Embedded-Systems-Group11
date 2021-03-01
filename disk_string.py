class DiskString:
    """Class representing the string and the disks on it

    Attributes
    __________
    goal_bin : int[1..*]
        the pattern according to which disks should be added to the string
    stringed_disks : int[*]
        represents the currently stringed disks
    iteration : int
        the number of times the pattern has been completed

    Methods
    _______
    next_disk() : int
        returns what color the next disk to be stringed should be
    string_disk(int) : bool
        adds disk to stringed disks, returns if stringed disk was correct color
    get_iteration() : int
        returns iteration
    """

    def __init__(self, goal_bin):
        self.goal_bin = goal_bin
        self.stringed_disks = []
        self.iteration = 0
