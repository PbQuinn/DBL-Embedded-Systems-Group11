from unittest import TestCase
from RPI.src.processor import Processor
from RPI.src.protocol_handler import ProtocolHandler
from RPI.src.expectation_handler import ExpectationHandler
from RPI.src.stringer import Stringer
from RPI.test.dummy_protocol_handler import DummyProtocolHandler


class TestInit(TestCase):

    def test_process_ping(self):
        # No expired outputs
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.processor.process(b"Motion Detected")
        for _ in range(9):
            self.assertEqual(self.processor.process(b"Ping"), [b"Pong"])
        # Expired outputs
        self.assertEqual(self.processor.process(b"Ping"), [[b"Retract Blocker"]])

    def test_process_motion(self):
        # Uncompleted stringer
        self.stringer = Stringer(0)
        self.processor = Processor(self.stringer, ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process(b"Motion Detected"), [b"Extend Blocker", b"Scan Color"])
        # Completed stringer
        self.stringer.stringed_disks = [0] * 8
        self.assertEqual(self.processor.process(b"Motion Detected"), [b"Ignore"])

    def test_process_white(self):
        # Unwanted color
        self.processor = Processor(Stringer(1), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process(b"White Detected"), [b"Retract Blocker"])
        # No permission from protocol
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(Stringer(0), self.protocol, ExpectationHandler())
        self.assertEqual(self.processor.process(b"White Detected"), [b"Retract Blocker"])
        # Wanted and permission
        self.protocol.set_allowance(True)
        self.assertEqual(self.processor.process(b"White Detected"), [b"Push", b"Retract Blocker"])

    def test_process_black(self):
        # Unwanted color
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process(b"Black Detected"), [b"Retract Blocker"])
        # No permission from protocol
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(Stringer(1), self.protocol, ExpectationHandler())
        self.assertEqual(self.processor.process(b"Black Detected"), [b"Retract Blocker"])
        # Wanted and permission
        self.protocol.set_allowance(True)
        self.assertEqual(self.processor.process(b"Black Detected"), [b"Push", b"Retract Blocker"])

    def test_process_unknown(self):
        self.processor = Processor(Stringer(69), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process(b"Test"), [b"Unknown Message"])
        self.assertEqual(self.processor.process(b"Gibberish"), [b"Unknown Message"])
