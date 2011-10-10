#! /usr/bin/env python

import unittest
import os

from locate import *

def setUpModule():
    os.mkdir("./test")
    os.mkdir("./test/lvl1")
    os.mkdir("./test/lvl2")
    os.mkdir("./test/lvl2/lvl3")
    open("./test/lvl2/testfile.txt", "w").close()
    open("./test/lvl2/lvl3/testfile1.txt", "w").close()

def tearDownModule():
    os.remove("./test/lvl2/testfile.txt")
    os.remove("./test/lvl2/lvl3/testfile1.txt")
    os.rmdir("./test/lvl1")
    os.removedirs("./test/lvl2/lvl3")
        
class LocateTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search_cwd(self):
        hits = locate("testfile.txt", "./test/")
        assert hits[:1] == ["./test/lvl2/testfile.txt"]

    def test_get_rating_full_match(self):
        name1 = "name"
        name2 = "name"
        rating = rate(name1, name2)
        assert rating == 1.0

    def test_get_rating_partial_match(self):
        name1 = "name"
        name2 = "myname"
        rating = rate(name2, name1)
        assert rating > 0.5
        assert rating < 1.0
        
        
if __name__ == "__main__":
    unittest.main()
