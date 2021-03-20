from RPI.src.communicator import CommunicatorSimulation, CommunicatorRobot
from RPI.src.processor import Processor
from RPI.src.string_handler import StringHandler
from RPI.src.protocol_handler import ProtocolHandler
from RPI.src.expectation_handler import ExpectationHandler


def get_number():
    while True:
        try:
            number = int(input('What number between 0 and 255 do you want to string? '))

            if 0 <= number <= 255:
                return number
            else:
                print("Incorrect input: number should be a non-negative integer.")
                continue

        except ValueError:
            print("Incorrect input: number should be a non-negative integer.")


def get_mode():
    while True:
        try:
            mode = str(input("Do you want to use the robot or simulation? [r/s] "))

            if mode == "r":
                return True
            elif mode == "s":
                return False
            else:
                print("Incorrect input: enter 'r' or 's'.")
                continue

        except ValueError:
            print("Incorrect input: enter 'r' or 's'.")


if __name__ == '__main__':
    sh = StringHandler(get_number())
    ph = ProtocolHandler()
    eh = ExpectationHandler()

    p = Processor(sh, ph, eh)

    if get_mode():
        print("Starting communication with robot...\n")
        cr = CommunicatorRobot(p)
        cr.start()
    else:
        print("Starting communication with simulation...\n")
        cs = CommunicatorSimulation(p)
        cs.start()
