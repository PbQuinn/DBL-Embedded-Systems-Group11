from unittest import TestCase
from RPI.src.processor import Processor
from RPI.src.protocol_handler import ProtocolHandler
from RPI.src.protocol_handler import DummyProtocolHandler
from RPI.src.expectation_handler import ExpectationHandler
from RPI.src.string_handler import StringHandler


class TestInit(TestCase):

    # Standalone ping
    def test_process_ping(self):
        # No expired outputs
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("in", ["out"], 5)
        for _ in range(4):
            self.assertEqual(["Pong"], self.processor.process("Ping"))
        # Expired outputs
        self.assertEqual(["Pong", "out"], self.processor.process("Ping"))
        self.expectations.add("a", ["0"], 0)
        self.expectations.add("b", ["1"], 0)
        self.assertEqual(["Pong", "1", "0"], self.processor.process("Ping"))

    # Conveyor belt
    def test_process_primary_motion(self):
        # Uncompleted stringer
        self.string_handler = StringHandler(0)
        self.processor = Processor(self.string_handler, ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Extend Blocker"], self.processor.process("Primary Motion"))
        # Completed stringer
        self.string_handler.stringed_disks = [0] * 8
        self.assertEqual(["Ignore"], self.processor.process("Primary Motion"))

    def test_process_blocker_extended(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Confirm Blocker Extended", ["Irrelevant"], 10)
        self.assertEqual(["Scan Primary Color"], self.processor.process("Confirm Blocker Extended"))

    def test_process_primary_white(self):
        # Unwanted color
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(1), ProtocolHandler(), self.expectations)
        self.expectations.add("Primary Color Detected", ["Irrelevant"], 10)
        self.assertEqual(["Retract Blocker"], self.processor.process("Primary White"))
        # No permission from protocol
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(StringHandler(0), self.protocol, self.expectations)
        self.expectations.add("Primary Color Detected", ["Irrelevant"], 10)
        self.assertEqual(["Retract Blocker"], self.processor.process("Primary White"))
        # Wanted and permission
        self.protocol = DummyProtocolHandler(True)
        self.expectations.add("Primary Color Detected", ["Irrelevant"], 10)
        self.assertEqual(["Push Pusher"], self.processor.process("Primary White"))

    def test_process_primary_black(self):
        # Unwanted color
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Primary Color Detected", ["Irrelevant"], 10)
        self.assertEqual(["Retract Blocker"], self.processor.process("Primary Black"))
        # No permission from protocol
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(StringHandler(1), self.protocol, self.expectations)
        self.expectations.add("Primary Color Detected", ["Irrelevant"], 10)
        self.assertEqual(["Retract Blocker"], self.processor.process("Primary Black"))
        # Wanted and permission
        self.protocol = DummyProtocolHandler(True)
        self.expectations.add("Primary Color Detected", ["Irrelevant"], 10)
        self.assertEqual(["Push Pusher"], self.processor.process("Primary Black"))

    def test_process_pusher_pushed(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Confirm Pusher Pushed", ["Irrelevant"], 10)
        self.assertEqual(["Retract Blocker"], self.processor.process("Confirm Pusher Pushed"))

    def test_process_blocker_retracted(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Confirm Blocker Retracted", ["Irrelevant"], 10)
        self.assertEqual(["Ignore"], self.processor.process("Confirm Blocker Retracted"))

    # Funnel to string
    def test_process_secondary_motion(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Secondary Motion", ["Irrelevant"], 10)
        self.assertEqual(["Scan Secondary Color"], self.processor.process("Secondary Motion"))

    def test_process_secondary_white(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Secondary White Detected", ["Irrelevant"], 10)
        self.assertEqual(["Push Stringer"], self.processor.process("Secondary White"))

    def test_process_secondary_black(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Secondary Black Detected", ["Irrelevant"], 10)
        self.assertEqual(["Push Stringer"], self.processor.process("Secondary Black"))

    def test_process_disk_stringed(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Tertiary Motion", ["Irrelevant"], 10)
        self.assertEqual(["Ignore"], self.processor.process("Tertiary Motion"))

    # Startup
    def test_process_white_set(self):
        # TODO
        self.fail("TODO")

    def test_process_black_set(self):
        # TODO
        self.fail("TODO")

    # Errors
    def test_process_error(self):
        # TODO
        self.fail("TODO")

    def test_process_unknown(self):
        self.processor = Processor(StringHandler(69), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Unknown Message"], self.processor.process("Test"))
        self.assertEqual(["Unknown Message"], self.processor.process("Gibberish"))

    def test_process_exception(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Error Occurred"], self.processor.process("Tertiary Motion"))
        self.assertEqual(["Error Occurred"], self.processor.process("Secondary Black"))
        self.assertEqual(["Error Occurred"], self.processor.process("Secondary White"))
        self.assertEqual(["Error Occurred"], self.processor.process("Secondary Motion"))
        self.assertEqual(["Error Occurred"], self.processor.process("Confirm Blocker Retracted"))
        self.assertEqual(["Error Occurred"], self.processor.process("Confirm Pusher Pushed"))
        self.assertEqual(["Error Occurred"], self.processor.process("Primary Black"))
        self.assertEqual(["Error Occurred"], self.processor.process("Primary White"))
        self.assertEqual(["Error Occurred"], self.processor.process("Confirm Blocker Extended"))
        