from unittest import TestCase
from RPI.src.disk_string import Stringer


class TestInit(TestCase):

    def test_constructor_exception(self):
        self.assertRaises(ValueError, Stringer, -1)

    def test_get_next_disk(self):
        # pattern consisting of only 1s, no disks stringed:
        self.stringer = Stringer(1)
        self.assertEqual(self.stringer.get_next_disk(), 1)
        # pattern consisting of only 0s, no disks stringed
        self.stringer = Stringer(0)
        self.assertEqual(self.stringer.get_next_disk(), 0)
        # pattern of length 3, one complete iteration:
        self.stringer = Stringer(6)
        self.assertEqual(self.stringer.get_next_disk(), 0)
        self.stringer.stringed_disks = [0]
        self.assertEqual(self.stringer.get_next_disk(), 1)
        self.stringer.stringed_disks = [1, 0]
        self.assertEqual(self.stringer.get_next_disk(), 1)
        self.stringer.stringed_disks = [1, 1, 0]
        self.assertEqual(self.stringer.get_next_disk(), 0)

    def test_string_disk(self):
        # pattern consisting of only 1s, stringing 1:
        self.stringer = Stringer(1)
        self.is_correct = self.stringer.string_disk(1)
        self.assertTrue(self.is_correct)
        self.assertEqual(self.stringer.stringed_disks, [1])
        # pattern consisting of only 1s, stringing 0:
        self.is_correct = self.stringer.string_disk(0)
        self.assertFalse(self.is_correct)
        self.assertEqual(self.stringer.stringed_disks, [0, 1])
        # pattern already partly stringed:
        self.stringer = Stringer(11)
        self.stringer.stringed_disks = [1, 1, 1, 0, 1, 1]
        self.is_correct = self.stringer.string_disk(0)
        self.assertTrue(self.is_correct)
        self.assertEqual(self.stringer.stringed_disks,
                         [0, 1, 1, 1, 0, 1, 1])
        self.is_correct = self.stringer.string_disk(0)
        self.assertFalse(self.is_correct)
        self.assertEqual(self.stringer.stringed_disks,
                         [0, 0, 1, 1, 1, 0, 1, 1])

    def test_get_iteration(self):
        # pattern length 1, no disks stringed:
        self.stringer = Stringer(1)
        self.assertEqual(self.stringer.get_iteration(), 0)
        self.stringer = Stringer(0)
        self.assertEqual(self.stringer.get_iteration(), 0)
        # pattern length 1, 2 disks stringed:
        self.stringer = Stringer(1)
        self.stringer.stringed_disks = [1, 0]
        self.assertEqual(self.stringer.get_iteration(), 2)
        # pattern length 3, 7 disks stringed:
        self.stringer = Stringer(4)
        self.stringer.stringed_disks = [1, 0, 0, 1, 0, 0, 1]
        self.assertEqual(self.stringer.get_iteration(), 2)
        # pattern length 7, 3 disks stringed:
        self.stringer = Stringer(73)
        self.stringer.stringed_disks = [1, 0, 0]
        self.assertEqual(self.stringer.get_iteration(), 0)

    def test_toBin_trivial(self):
        self.stringer = Stringer(1)
        arr_check = [1]
        check = True
        if len(arr_check) != len(self.stringer.pattern):
            check = False
        if arr_check[0] != self.stringer.pattern[0]:
            check = False
        self.assertTrue(check)

    def test_toBin_not_trivial(self):
        self.stringer = Stringer(54)
        arr_check = [1, 1, 0, 1, 1, 0]
        check = True
        if len(arr_check) != len(self.stringer.pattern):
            check = False
        for i in arr_check:
            if arr_check[i] != self.stringer.pattern[i]:
                check = False
        self.assertTrue(check)