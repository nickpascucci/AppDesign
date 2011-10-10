#! /usr/bin/env python

"""Unit tests for bookmark objects."""

import unittest
from bookmark import Bookmark

__author__ = "Nick Pascucci (npascut1@gmail.com"

class BookmarkTest(unittest.TestCase):
    def setUp(self):
        self.bkmk = Bookmark("GNU", "http://www.gnu.org/", "1318111005")

    def tearDown(self):
        pass

    def test_to_link(self):
        link = self.bkmk.to_link()
        good_lnk = '<A HREF="http://www.gnu.org/" ADD_DATE="1318111005">GNU</A>'
        assert link == good_lnk
        
    def test_str(self):
        string_val = str(self.bkmk)
        good_string = "GNU: http://www.gnu.org/\tCreated: 2011-10-08-15-56"
        assert string_val == good_string
        
if __name__ == "__main__":
    unittest.main()
