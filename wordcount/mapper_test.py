#! /usr/bin/env python
"""Unit tests for the word count mapper."""

import unittest
from mapper import *
from mock_socket import MockSocket

__author__ = "Nick Pascucci (npascut1@gmail.com)"

class MapperTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_tokenize_string(self):
        data = "The quick brown fox - jumped over the lazy dog."
        tokens = tokenize(data)
        assert tokens == ["the", "quick", "brown", "fox", "jumped", "over",
                          "the", "lazy", "dog"]

    def test_tokenize_removes_null(self):
        data = "abc\0"
        tokens = tokenize(data)
        assert tokens == ["abc"]

    def test_map_on_token(self):
        token = "abc"
        output = map_token(token)
        assert output == ("abc", 1)
        
    def test_execute(self):
        source = MockSocket()
        source.data = "HELLO, world!\0"
        sink = MockSocket()
        execute(source, sink)
        assert sink.sent == '{"hello": 1}{"world": 1}\0'

if __name__ == "__main__":
    unittest.main()
