#! /usr/bin/env python
"""Unit tests for the word count reducer/sink."""

import unittest

from reducer import *

class ReducerTest(unittest.TestCase):
    def setUp(self):
        self.reducer = Reducer()

    def tearDown(self):
        pass

    def test_parse_object(self):
        token = '{"abc": 1}'
        obj = parse_object(token)
        assert obj == ("abc", 1)

    def test_get_next_object_complete(self):
        buf = '{"abc": 1}{"def": 1}'
        token = get_next_object(buf)
        assert token == '{"abc": 1}'

    def test_get_next_object_none(self):
        buf = ''
        token = get_next_object(buf)
        assert not token

    def test_reduce(self):
        vals = [("abc", 1), ("abc", 1), ("def", 1)]
        for val in vals:
            self.reducer.reduce(val)
        assert self.reducer.vals == {"abc": 2, "def": 1}

    def test_get_next_mapping(self):
        buf = '{"abc": 1}{"def": 1}'
        mapping, buf = get_next_mapping(buf)
        assert mapping == ("abc", 1)
        assert buf == '{"def": 1}'
        
if __name__ == "__main__":
    unittest.main()

