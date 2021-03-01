from unittest import TestCase
from main import Stringer


class TestInit(TestCase):
    def test_goalInt(self):
        self.stringer = Stringer(1)
        self.assertEqual(self.stringer.goalInt, 1)

    def test_stoneCounter(self):
        self.stringer = Stringer(1)
        self.assertEqual(self.stringer.stoneCounter, 0)

    def test_toBin_trivial(self):
        self.stringer = Stringer(1)
        arr_check = [1]
        check = True
        if(len(arr_check) != len(self.stringer.goalBin)):
            check = False
        if(arr_check[0] != self.stringer.goalBin[0]):
            check = False
        self.assertTrue(check)

    def test_toBin_not_trivial(self):
        self.stringer = Stringer(54)
        arr_check = [1, 1, 0, 1, 1, 0]
        check = True
        if len(arr_check) != len(self.stringer.goalBin):
            check = False
        for i in arr_check:
            if arr_check[i] != self.stringer.goalBin[i]:
                check = False
        self.assertTrue(check)
