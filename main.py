# The main class that will be setup and then will run all interactions
class Stringer:
    def __init__(self, goalInt):
        self.goalInt = goalInt
        self.stoneCounter = 0
        self.goalBin = []
        self.toBin()

    """ converts the goal into a array which represents the number in a integer format
    :param self, a Stringer class with a valid goalInt
    :pre goalInt > 0
    :modifies goalBin
    :post @code{for 0<i<goalBin.len goal = goalbin[i] * 2**i, goal ==goalInt}
    """

    def toBin(self):
        goal = self.goalInt
        while goal > 0:
            if goal % 2 == 1:
                self.goalBin.insert(0, 1)
                goal = goal // 2
                print(goal)
            else:
                self.goalBin.insert(0, 0)
                goal = goal // 2
                print(goal)


if __name__ == '__main__':
    validInteger = False
    while not validInteger:
        try:
            number = int(input('Enter a positive integer to use:'))
            if number > 0:
                validInteger = True
                print('We will use ' + str(number))
            else:
                print('The integer must be positive')
        except ValueError:
            print('We require a positive integer')
    myStringer = Stringer(number)
    print(myStringer.goalBin)
