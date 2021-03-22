from RPI.src.communicator import CommunicatorSimulation, CommunicatorRobot
from RPI.src.processor import Processor
from RPI.src.string_handler import StringHandler
from RPI.src.protocol_handler import ProtocolHandler
from RPI.src.protocol_handler import DummyProtocolHandler
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


def choose_protocol_handler():
    while True:
        try:
            mode = str(input("Do you want to connect to the protocol or use a dummy? [p/d] "))

            if mode == "p":
                return ProtocolHandler()
            elif mode == "d":
                return DummyProtocolHandler(True)
            else:
                print("Incorrect input: enter 'p' or 'd'.")
                continue

        except ValueError:
            print("Incorrect input: enter 'p' or 'd'.")


def setup_processor(protocol_handler):
    s = StringHandler(get_number())
    ph = protocol_handler
    eh = ExpectationHandler()
    return Processor(s, ph, eh)


if __name__ == '__main__':

    if get_mode():
        p = setup_processor(choose_protocol_handler())
        print("Starting communication with robot...\n")
        cr = CommunicatorRobot(p)
        cr.start()
    else:
        p = setup_processor(choose_protocol_handler())
        print("Starting communication with simulation...\n")
        cs = CommunicatorSimulation(p)
        cs.start()
