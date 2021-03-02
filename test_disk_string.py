from unittest import TestCase
from disk_string import DiskString


class TestInit(TestCase):

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

    def test_constructor_exception(self):
        empty_pattern = []
        self.assertRaises(ValueError, DiskString, empty_pattern)


# TODO add more test cases for DiskString