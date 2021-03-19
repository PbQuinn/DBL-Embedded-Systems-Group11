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
        self.processor.process("Motion Detected")
        for _ in range(9):
            self.assertEqual(self.processor.process("Ping"), ["Pong"])
        # Expired outputs
        self.assertEqual(self.processor.process("Ping"), ["Pong", ["Retract Blocker"]])

    def test_process_motion_detected(self):
        # Uncompleted stringer
        self.stringer = Stringer(0)
        self.processor = Processor(self.stringer, ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Motion Detected"), ["Extend Blocker"])
        # Completed stringer
        self.stringer.stringed_disks = [0] * 8
        self.assertEqual(self.processor.process("Motion Detected"), ["Ignore"])

    def test_process_white_detected(self):
        # Unwanted color
        self.processor = Processor(Stringer(1), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("White Detected"), ["Retract Blocker"])
        # No permission from protocol
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(Stringer(0), self.protocol, ExpectationHandler())
        self.assertEqual(self.processor.process("White Detected"), ["Retract Blocker"])
        # Wanted and permission
        self.protocol.set_allowance(True)
        self.assertEqual(self.processor.process("White Detected"), ["Push", "Retract Blocker"])

    def test_process_black_detected(self):
        # Unwanted color
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Black Detected"), ["Retract Blocker"])
        # No permission from protocol
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(Stringer(1), self.protocol, ExpectationHandler())
        self.assertEqual(self.processor.process("Black Detected"), ["Retract Blocker"])
        # Wanted and permission
        self.protocol.set_allowance(True)
        self.assertEqual(self.processor.process("Black Detected"), ["Push", "Retract Blocker"])

    def test_process_blocker_extended(self):
        # Not yet expected
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Blocker Extended"), ["Unexpected Message"])
        # Expected
        self.processor.process("Motion Detected")
        self.assertEqual(self.processor.process("Blocker Extended"), ["Scan Color"])
        # No longer expected
        self.assertEqual(self.processor.process("Blocker Extended"), ["Unexpected Message"])

    def test_process_blocker_retracted(self):
        # Not yet expected
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Blocker Retracted"), ["Unexpected Message"])
        # Expected
        self.processor.process("Motion Detected")
        self.processor.process("Blocker Extended")
        self.processor.process("White Detected")
        self.assertEqual(self.processor.process("Blocker Retracted"), ["???"])
        # No longer expected
        self.assertEqual(self.processor.process("Blocker Retracted"), ["Unexpected Message"])

    def test_process_pusher_pushed(self):
        # Not yet expected
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Pusher Pushed"), ["Unexpected Message"])
        # Expected
        self.processor.process("Motion Detected")
        self.processor.process("Blocker Extended")
        self.processor.process("White Detected")
        self.assertEqual(self.processor.process("Pusher Pushed"), ["???"])
        # No longer expected
        self.assertEqual(self.processor.process("Pusher Pushed"), ["Unexpected Message"])

    def test_process_disk_stringed(self):
        # Not yet expected
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Disk Stringed"), ["Unexpected Message"])
        # Expected
        self.processor.process("Motion Detected")
        self.processor.process("Blocker Extended")
        self.processor.process("White Detected")
        self.processor.process("Pusher Pushed")
        self.assertEqual(self.processor.process("Disk Stringed"), ["???"])
        # No longer expected
        self.assertEqual(self.processor.process("Disk Stringed"), ["Unexpected Message"])

    def test_process_white_set(self):
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("White Set"), ["???"])

    def test_process_black_set(self):
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Black Set"), ["???"])

    def test_process_error(self):
        self.processor = Processor(Stringer(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Error Occurred"), ["???"])

    def test_process_unknown(self):
        self.processor = Processor(Stringer(69), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(self.processor.process("Test"), ["Unknown Message"])
        self.assertEqual(self.processor.process("Gibberish"), ["Unknown Message"])
