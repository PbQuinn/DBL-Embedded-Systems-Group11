from unittest import TestCase
from disk_string import DiskString


class TestInit(TestCase):

    def test_constructor_exception(self):
        empty_pattern = []
        self.assertRaises(ValueError, DiskString, empty_pattern)

    def test_get_next_disk(self):
        # pattern consisting of only 1s, no disks stringed:
        self.disk_string = DiskString([1])
        self.assertEqual(self.disk_string.get_next_disk(), 1)
        # pattern consisting of only 0s, no disks stringed
        self.disk_string = DiskString([0])
        self.assertEqual(self.disk_string.get_next_disk(), 0)
        # pattern of length 3, one complete iteration:
        self.disk_string = DiskString([1, 1, 0])
        self.assertEqual(self.disk_string.get_next_disk(), 0)
        self.disk_string.stringed_disks = [0]
        self.assertEqual(self.disk_string.get_next_disk(), 1)
        self.disk_string.stringed_disks = [1, 0]
        self.assertEqual(self.disk_string.get_next_disk(), 1)
        self.disk_string.stringed_disks = [1, 1, 0]
        self.assertEqual(self.disk_string.get_next_disk(), 0)

    def test_string_disk(self):
        # pattern consisting of only 1s, stringing 1:
        self.disk_string = DiskString([1])
        self.is_correct = self.disk_string.string_disk(1)
        self.assertTrue(self.is_correct)
        self.assertEqual(self.disk_string.stringed_disks, [1])
        # pattern consisting of only 1s, stringing 0:
        self.is_correct = self.disk_string.string_disk(0)
        self.assertFalse(self.is_correct)
        self.assertEqual(self.disk_string.stringed_disks, [0, 1])
        # pattern already partly stringed:
        self.disk_string = DiskString([1, 0, 1, 1])
        self.disk_string.stringed_disks = [1, 1, 1, 0, 1, 1]
        self.is_correct = self.disk_string.string_disk(0)
        self.assertTrue(self.is_correct)
        self.assertEqual(self.disk_string.stringed_disks,
                         [0, 1, 1, 1, 0, 1, 1])
        self.is_correct = self.disk_string.string_disk(0)
        self.assertFalse(self.is_correct)
        self.assertEqual(self.disk_string.stringed_disks,
                         [0, 0, 1, 1, 1, 0, 1, 1])

    def test_get_iteration(self):
        # pattern length 1, no disks stringed:
        self.disk_string = DiskString([1])
        self.assertEqual(self.disk_string.get_iteration(), 0)
        self.disk_string = DiskString([0])
        self.assertEqual(self.disk_string.get_iteration(), 0)
        # pattern length 1, 2 disks stringed:
        self.disk_string = DiskString([1])
        self.disk_string.stringed_disks = [1, 0]
        self.assertEqual(self.disk_string.get_iteration(), 2)
        # pattern length 3, 7 disks stringed:
        self.disk_string = DiskString([1, 0, 0])
        self.disk_string.stringed_disks = [1, 0, 0, 1, 0, 0, 1]
        self.assertEqual(self.disk_string.get_iteration(), 2)
        # pattern length 7, 3 disks stringed:
        self.disk_string = DiskString([1, 0, 0, 1, 0, 0, 1])
        self.disk_string.stringed_disks = [1, 0, 0]
        self.assertEqual(self.disk_string.get_iteration(), 0)