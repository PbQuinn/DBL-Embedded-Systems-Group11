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
        self.expectations.add("in", 5, "TEST MESSAGE")
        for _ in range(4):
            self.assertEqual(["Pong"], self.processor.process("Ping"))
        # Expired outputs
        self.assertEqual(["Enter Error Mode"], self.processor.process("Ping"))
        self.assertEqual(["Pong"], self.processor.process("Ping"))
        self.expectations.add("new", 0, "TEST MESSAGE")
        self.assertEqual(["Enter Error Mode"], self.processor.process("Ping"))

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
        self.expectations.add("Confirm Blocker Extended", 10, "TEST MESSAGE")
        self.assertEqual(["Scan Primary Color"], self.processor.process("Confirm Blocker Extended"))

    def test_process_primary_white(self):
        # Unwanted color
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(1), ProtocolHandler(), self.expectations)
        self.expectations.add("Primary Color Detected", 10, "TEST MESSAGE")
        self.assertEqual(["Retract Blocker"], self.processor.process("Primary White"))
        # No permission from protocol
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(StringHandler(0), self.protocol, self.expectations)
        self.expectations.add("Primary Color Detected", 10, "TEST MESSAGE")
        self.assertEqual(["Retract Blocker"], self.processor.process("Primary White"))
        # Wanted and permission
        self.protocol = DummyProtocolHandler(True)
        self.processor = Processor(StringHandler(0), self.protocol, self.expectations)
        self.expectations.add("Primary Color Detected", 10, "TEST MESSAGE")
        self.assertEqual(["Push Pusher"], self.processor.process("Primary White"))

    def test_process_primary_black(self):
        # Unwanted color
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Primary Color Detected", 10, "TEST MESSAGE")
        self.assertEqual(["Retract Blocker"], self.processor.process("Primary Black"))
        # No permission from protocol
        self.protocol = DummyProtocolHandler(False)
        self.processor = Processor(StringHandler(1), self.protocol, self.expectations)
        self.expectations.add("Primary Color Detected", 10, "TEST MESSAGE")
        self.assertEqual(["Retract Blocker"], self.processor.process("Primary Black"))
        # Wanted and permission
        self.protocol = DummyProtocolHandler(True)
        self.processor = Processor(StringHandler(1), self.protocol, self.expectations)
        self.expectations.add("Primary Color Detected", 10, "TEST MESSAGE")
        self.assertEqual(["Push Pusher"], self.processor.process("Primary Black"))

    def test_process_pusher_pushed(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Confirm Pusher Pushed", 10, "TEST MESSAGE")
        self.assertEqual(["Retract Blocker"], self.processor.process("Confirm Pusher Pushed"))

    def test_process_blocker_retracted(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Confirm Blocker Retracted", 10, "TEST MESSAGE")
        self.assertEqual(["Ignore"], self.processor.process("Confirm Blocker Retracted"))

    # Funnel to string
    def test_process_secondary_motion(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Secondary Motion", 10, "TEST MESSAGE")
        self.assertEqual(["Scan Secondary Color"], self.processor.process("Secondary Motion"))

    def test_process_secondary_white(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Secondary White Detected", 10, "TEST MESSAGE")
        self.assertEqual(["Push Stringer"], self.processor.process("Secondary White"))

    def test_process_secondary_black(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Secondary Black Detected", 10, "TEST MESSAGE")
        self.assertEqual(["Push Stringer"], self.processor.process("Secondary Black"))

    def test_process_disk_stringed(self):
        self.expectations = ExpectationHandler()
        self.processor = Processor(StringHandler(0), ProtocolHandler(), self.expectations)
        self.expectations.add("Tertiary Motion", 10, "TEST MESSAGE")
        self.assertEqual(["Ignore"], self.processor.process("Tertiary Motion"))

    # Errors
    def test_process_primary_neither(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Primary Neither"))

    def test_process_secondary_neither(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Secondary Neither"))

    def test_process_error_string_disk(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Error String Disk"))

    def test_process_unexpected_error(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Unexpected Error Occurred"))

    def test_process_illegal_command(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Illegal Command Sent"))

    def test_process_unknown_command(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Unknown Command Sent"))

    def test_process_message_buffer_full(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Message Buffer Full"))

    def test_process_unknown(self):
        self.processor = Processor(StringHandler(69), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Test"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Gibberish"))

    def test_process_exception(self):
        self.processor = Processor(StringHandler(0), ProtocolHandler(), ExpectationHandler())
        self.assertEqual(["Enter Error Mode"], self.processor.process("Tertiary Motion"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Secondary Black"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Secondary White"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Secondary Motion"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Confirm Blocker Retracted"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Confirm Pusher Pushed"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Primary Black"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Primary White"))
        self.assertEqual(["Enter Error Mode"], self.processor.process("Confirm Blocker Extended"))
