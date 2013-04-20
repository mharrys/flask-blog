import unittest
import re

from app.helpers import is_name, slugify
from datetime import datetime


class TestHelpers(unittest.TestCase):

    def test_is_name(self):
        sep = [' ', '-', '_']  # valid name seperators
        ok_name = ['name', 'nAmE', 'NAME', 'n4m3', '1234']
        nok_name = ['n@me', 'name$', '*name', 'nAme ', ' naMe']
        r = re.compile(is_name.regex)
        # test all possible name combinations with the name seperator
        for name1 in ok_name:
            self.assertIsNotNone(r.match(name1))
            for name2 in ok_name:
                self.assertIsNotNone(r.match(name2))
                for s in sep:
                    self.assertIsNotNone(r.match(name1 + s + name2))
                    self.assertIsNone(r.match(name1 + s + s + name2))
        for name1 in nok_name:
            self.assertIsNone(r.match(name1))
            for name2 in nok_name:
                self.assertIsNone(r.match(name2))
                for s in sep:
                    self.assertIsNone(r.match(name1 + s + name2))
                    self.assertIsNone(r.match(name1 + s + s + name2))

    def test_slugify(self):
        slug = slugify(datetime(2013, 1, 20), u'Title!')
        self.assertEqual('2013/1/20/title', slug)
        slug = slugify(datetime(2011, 8, 12), u'Title Title')
        self.assertEqual('2011/8/12/title-title', slug)
        slug = slugify(datetime(2012, 10, 2), u' T1tl3!  T1tl3! ')
        self.assertEqual('2012/10/2/t1tl3-t1tl3', slug)
