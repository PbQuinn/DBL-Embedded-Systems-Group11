from abc import ABC, abstractmethod
import zmq


class Server(ABC):

    _processor = None
    _running = False

    def __init__(self, processor):
        self._processor = processor

    @abstractmethod
    def _run(self):
        pass

    def set_running(self, running):
        self._running = running

    def get_running(self):
        return self._running


class ServerSimulation(Server):

    def __init__(self, processor):
        # Call super constructor
        Server.__init__(self, processor)

        # Create and bind socket
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

    def _run(self):
        self._running = True

        while self._running:
            # Receive
            msg_receive = self.socket.recv()
            print("Received: %s" % msg_receive)

            # Process
            msg_send = self._processor.process(msg_receive)

            # Send
            self.socket.send(msg_send)
            print("Sent: %s" % msg_send)


class ServerRobot(Server):

    def __init__(self, processor):
        Server.__init__(self, processor)

    def _run(self):
        pass
