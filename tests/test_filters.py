import unittest

from app import pluralize


class TestFilters(unittest.TestCase):

    def test_pluralize(self):
        # defaults
        one, many = '', 's'
        self.assertEqual(many, pluralize(0))
        self.assertEqual(one, pluralize(1))
        self.assertEqual(many, pluralize(32))
        # defaults with negative values
        self.assertEqual(one, pluralize(-1))
        self.assertEqual(many, pluralize(-13))
        # custom suffix (for entry, entries etc.)
        one, many = 'y', 'ies'
        self.assertEqual(many, pluralize(0, one, many))
        self.assertEqual(one, pluralize(1, one, many))
        self.assertEqual(many, pluralize(27, one, many))
        # negative with custom suffix
        self.assertEqual(one, pluralize(-1, one, many))
        self.assertEqual(many, pluralize(-72, one, many))
