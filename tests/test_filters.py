import unittest

from app import pluralize, timesince
from datetime import datetime


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

    def test_timesince(self):
        year, month, day, hour, minute, second = 2012, 6, 12, 8, 34, 24
        now = datetime(year, month, day, hour, minute, second)
        # years
        then = datetime(year - 1, month, day)
        self.assertEqual('1 year', timesince(then, now))
        then = datetime(year - 5, month, day)
        self.assertEqual('5 years', timesince(then, now))
        # month
        then = datetime(year, month - 1, day)
        self.assertEqual('1 month', timesince(then, now))
        # acceptable approximation error, off by roughly 1 day
        then = datetime(year, month - 3, day - 1)
        self.assertEqual('3 months', timesince(then, now))
        then = datetime(year, month - 5, day - 1)
        self.assertEqual('5 months', timesince(then, now))
        # day
        then = datetime(year, month, day - 1)
        self.assertEqual('1 day', timesince(then, now))
        then = datetime(year, month, day - 10)
        self.assertEqual('10 days', timesince(then, now))
        # hour
        then = datetime(year, month, day, hour - 1)
        self.assertEqual('1 hour', timesince(then, now))
        then = datetime(year, month, day, hour - 7)
        self.assertEqual('7 hours', timesince(then, now))
        # minute
        then = datetime(year, month, day, hour, minute - 1)
        self.assertEqual('1 minute', timesince(then, now))
        then = datetime(year, month, day, hour, minute - 30)
        self.assertEqual('30 minutes', timesince(then, now))
        # second
        then = datetime(year, month, day, hour, minute, second)
        self.assertEqual('0 seconds', timesince(then, now))
        then = datetime(year, month, day, hour, minute, second - 1)
        self.assertEqual('1 second', timesince(then, now))
        then = datetime(year, month, day, hour, minute, second - 18)
        self.assertEqual('18 seconds', timesince(then, now))
