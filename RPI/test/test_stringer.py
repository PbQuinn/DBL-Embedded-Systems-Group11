from unittest import TestCase
from RPI.src.stringer import Stringer


class TestInit(TestCase):

    def test_constructor_exception(self):
        self.assertRaises(ValueError, Stringer, -1)
        self.assertRaises(ValueError, Stringer, 256)

    def test_get_next_color(self):
        # pattern consisting of only 1s, no disks stringed:
        self.stringer = Stringer(255)
        self.assertEqual(self.stringer.get_next_color(), 1)
        # pattern consisting of only 0s, no disks stringed:
        self.stringer = Stringer(0)
        self.assertEqual(self.stringer.get_next_color(), 0)
        # pattern 6 = [0, 0, 0, 0, 0, 1, 1, 0]_2, stringed completely:
        self.stringer = Stringer(6)
        self.assertEqual(self.stringer.get_next_color(), 0)
        self.stringer.stringed_disks = [0]
        self.assertEqual(self.stringer.get_next_color(), 1)
        self.stringer.stringed_disks = [1, 0]
        self.assertEqual(self.stringer.get_next_color(), 1)
        self.stringer.stringed_disks = [1, 1, 0]
        for i in range(5):
            self.assertEqual(self.stringer.get_next_color(), 0)
            self.stringer.stringed_disks.insert(0, 0)

    def test_get_next_color_exception(self):
        self.stringer = Stringer(6)
        self.stringer.stringed_disks = [0, 0, 0, 0, 0, 1, 1, 0]
        self.assertRaises(Exception, self.stringer.get_next_color)

    def test_string_disk(self):
        # pattern consisting of only 1s, stringing 1:
        self.stringer = Stringer(255)
        self.is_correct = self.stringer.string_disk(1)
        self.assertTrue(self.is_correct)
        self.assertEqual(self.stringer.stringed_disks, [1])
        # pattern consisting of only 1s, stringing 0:
        self.stringer = Stringer(255)
        self.is_correct = self.stringer.string_disk(0)
        self.assertFalse(self.is_correct)
        self.assertEqual(self.stringer.stringed_disks, [0])
        # pattern already partly stringed:
        self.stringer = Stringer(11)
        self.stringer.stringed_disks = [1, 1]
        self.is_correct = self.stringer.string_disk(0)
        self.assertTrue(self.is_correct)
        self.assertEqual(self.stringer.stringed_disks, [0, 1, 1])
        self.is_correct = self.stringer.string_disk(0)
        self.assertFalse(self.is_correct)
        self.assertEqual(self.stringer.stringed_disks, [0, 0, 1, 1])

    def test_to_string_exception(self):
        self.stringer = Stringer(11)
        self.stringer.stringed_disks = [0, 0, 0, 0, 1, 0, 1, 1]
        self.assertRaises(Exception, self.stringer.string_disk, 1)
        self.assertRaises(Exception, self.stringer.string_disk, 0)

    def test_to_bin_0(self):
        self.stringer = Stringer(1)
        arr_check = [0, 0, 0, 0, 0, 0, 0, 0]
        check = True
        if len(arr_check) != len(self.stringer.pattern):
            check = False
        if arr_check[0] != self.stringer.pattern[0]:
            check = False
        self.assertTrue(check)

    def test_to_bin_1(self):
        self.stringer = Stringer(1)
        arr_check = [0, 0, 0, 0, 0, 0, 0, 1]
        check = True
        if len(arr_check) != len(self.stringer.pattern):
            check = False
        if arr_check[0] != self.stringer.pattern[0]:
            check = False
        self.assertTrue(check)

    def test_to_bin_255(self):
        self.stringer = Stringer(255)
        arr_check = [1, 1, 1, 1, 1, 1, 1, 1]
        check = True
        if len(arr_check) != len(self.stringer.pattern):
            check = False
        if arr_check[0] != self.stringer.pattern[0]:
            check = False
        self.assertTrue(check)

    def test_to_bin_54(self):
        self.stringer = Stringer(54)
        arr_check = [0, 0, 1, 1, 0, 1, 1, 0]
        check = True
        if len(arr_check) != len(self.stringer.pattern):
            check = False
        for i in arr_check:
            if arr_check[i] != self.stringer.pattern[i]:
                check = False
        self.assertTrue(check)

    def test_is_complete_trivial(self):
        # empty string, pattern only 1s
        self.stringer = Stringer(255)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(1)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.stringed_disks = [1, 1, 1, 1, 1, 1, 1]
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(1)
        self.assertTrue(self.stringer.is_complete())

    def test_is_complete_not_trivial(self):
        # pattern 19 = [0, 0, 0, 1, 0, 0, 1, 1]_2, stringed to completion
        self.stringer = Stringer(19)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(1)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(1)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(0)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(0)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(1)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(0)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(0)
        self.assertFalse(self.stringer.is_complete())
        self.stringer.string_disk(0)
        self.assertTrue(self.stringer.is_complete())

    def test_should_pickup_trivial(self):
        # empty string, pattern all 1s
        self.stringer = Stringer(255)
        self.assertTrue(self.stringer.should_pickup(1))
        self.assertFalse(self.stringer.should_pickup(0))
        # empty string, pattern all 0s
        self.stringer = Stringer(0)
        self.assertFalse(self.stringer.should_pickup(1))
        self.assertTrue(self.stringer.should_pickup(0))

    def test_should_pickup_not_trivial(self):
        # pattern 13 = [0, 0, 0, 0, 1, 1, 0, 1]_2
        self.stringer = Stringer(13)
        self.assertTrue(self.stringer.should_pickup(1))
        self.assertFalse(self.stringer.should_pickup(0))
        self.stringer.string_disk(1)
        self.assertFalse(self.stringer.should_pickup(1))
        self.assertTrue(self.stringer.should_pickup(0))
        self.stringer.string_disk(0)
        self.assertTrue(self.stringer.should_pickup(1))
        self.assertFalse(self.stringer.should_pickup(0))
        self.stringer.string_disk(1)
        self.assertTrue(self.stringer.should_pickup(1))
        self.assertFalse(self.stringer.should_pickup(0))



