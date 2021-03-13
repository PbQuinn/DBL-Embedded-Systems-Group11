from unittest import TestCase
from RPI.src.processor import Processor
from RPI.src.protocol_handler import ProtocolHandler
from RPI.src.expectation_handler import ExpectationHandler
from RPI.src.stringer import Stringer
from RPI.test.dummy_protocol_handler import DummyProtocolHandler


class TestInit(TestCase):

    def test_process_ping(self):
        # No expired outputs
        self.processor = Processor(ProtocolHandler(), ExpectationHandler())
        self.processor.set_stringer(Stringer(0))
        self.processor.process(b"Motion Detected")
        for _ in range(9):
            self.assertEqual(self.processor.process(b"Ping"), [b"Pong"])
        # Expired outputs
        self.assertEqual(self.processor.process(b"Ping"), [[b"Retract Blocker"]])

    def test_process_motion(self):
        # Uncompleted stringer
        self.processor = Processor(ProtocolHandler(), ExpectationHandler())
        self.stringer = Stringer(0)
        self.processor.set_stringer(self.stringer)
        self.assertEqual(self.processor.process(b"Motion Detected"), [b"Extend Blocker", b"Scan Color"])
        # Completed stringer
        self.stringer.stringed_disks = [0]
        self.assertEqual(self.processor.process(b"Motion Detected"), [b"Ignore"])

    def test_process_white(self):
        # Unwanted color
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(self.protocol, ExpectationHandler())
        self.processor.set_stringer(Stringer(1))
        self.assertEqual(self.processor.process(b"White Detected"), [b"Retract Blocker"])
        # No permission from protocol
        self.processor.set_stringer(Stringer(0))
        self.assertEqual(self.processor.process(b"White Detected"), [b"Retract Blocker"])
        # Wanted and permission
        self.protocol.set_allowance(True)
        self.assertEqual(self.processor.process(b"White Detected"), [b"Push", b"Retract Blocker"])

    def test_process_black(self):
        # Unwanted color
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(self.protocol, ExpectationHandler())
        self.processor.set_stringer(Stringer(0))
        self.assertEqual(self.processor.process(b"Black Detected"), [b"Retract Blocker"])
        # No permission from protocol
        self.processor.set_stringer(Stringer(1))
        self.assertEqual(self.processor.process(b"Black Detected"), [b"Retract Blocker"])
        # Wanted and permission
        self.protocol.set_allowance(True)
        self.assertEqual(self.processor.process(b"Black Detected"), [b"Push", b"Retract Blocker"])

    def test_process_unknown(self):
        self.processor = Processor(ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process(b"Test"), [b"Unknown Message"])
        self.assertEqual(self.processor.process(b"Gibberish"), [b"Unknown Message"])
