from unittest import TestCase
from RPI.src.expectation_handler import ExpectationHandler


class TestInit(TestCase):

    def test_add(self):
        self.handler = ExpectationHandler()
        self.handler.add("input", ["output"], 10)
        self.handler.add("0", ["1", "2", "3"], 4)
        self.handler.add("empty", [], 8)

    def test_remove(self):
        # Unexpected input
        self.handler = ExpectationHandler()
        self.assertRaises(ValueError, self.handler.remove, "input")
        self.assertRaises(ValueError, self.handler.remove, "unknown")
        # Expected input
        self.handler.add("input", ["output"], 10)
        self.handler.add("empty", [], 5)  # Possible, but not wanted by simulation
        self.handler.add("multi", ["0", "1", "2"], 3)
        self.handler.remove("input")
        self.handler.remove("empty")
        self.handler.remove("multi")

    def test_get_expired_outputs(self):
        # No expired outputs
        self.handler = ExpectationHandler()
        self.assertEqual([], self.handler.get_expired_outputs())
        self.handler.add("uno", ["one"], 1)
        self.handler.add("dos", ["two", "twee"], 2)
        self.handler.add("empty", [], 2)
        self.handler.add("hola", ["hello"], 2)
        self.handler.add("remove", ["gone"], 2)
        self.assertEqual([], self.handler.get_expired_outputs())
        # Expired outputs
        self.handler.ping()
        self.assertEqual(["one"], self.handler.get_expired_outputs())
        self.handler.remove("remove")
        self.handler.ping()
        self.assertEqual(["hello", "two", "twee"], self.handler.get_expired_outputs())
