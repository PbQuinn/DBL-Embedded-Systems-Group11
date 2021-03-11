from unittest import TestCase
from RPI.src.main import Main


class TestInit(TestCase):

    def test_goalInt(self):
        self.stringer = Stringer(1)
        self.assertEqual(self.stringer.goal_int, 1)

    def test_stoneCounter(self):
        self.stringer = Stringer(1)
        self.assertEqual(self.stringer.disk_counter, 0)


