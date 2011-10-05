#! /usr/bin/env python
"""Unit tests for the stats program."""

__author__ = "Nick Pascucci (npascut1@gmail.com)"

import unittest
from AppDesign.stats.stats import *

ACCEPTABLE_ERROR = .0001

class StatsTest(unittest.TestCase):
    def setUp(self):
        self.int_sequence = [1, 2, 3, 4, 5, 6]
        self.float_sequence = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        self.avg = 3.50
        self.std_dev = 1.70783
        
    def tearDown(self):
        pass

    def test_get_average_returns_average_for_ints(self):
        avg = get_avg(self.int_sequence)
        assert avg == self.avg

    def test_get_average_returns_average_for_floats(self):
        avg = get_avg(self.float_sequence)
        assert avg == self.avg
        
    def test_get_std_dev_returns_std_dev_for_ints(self):
        std_dev = get_std_dev(self.int_sequence)
        error = abs(std_dev - self.std_dev)
        assert error < ACCEPTABLE_ERROR

    def test_get_std_dev_returns_std_def_for_floats(self):
        std_dev = get_std_dev(self.float_sequence)
        error = abs(std_dev - self.std_dev)
        assert error < ACCEPTABLE_ERROR
    
    def test_get_stats_returns_stats(self):
        stats = get_stats(self.int_sequence)
        assert stats == (self.int_sequence[0],
                         self.int_sequence[-1],
                         get_avg(self.int_sequence),
                         get_std_dev(self.int_sequence)
                         )
    def test_get_avg_does_not_modify_sequence(self):
        self.int_sequence.reverse()
        old_sequence = self.int_sequence[:]
        get_avg(self.int_sequence)
        assert self.int_sequence == old_sequence

    def test_get_std_dev_does_not_modify_sequence(self):
        self.int_sequence.reverse()
        old_sequence = self.int_sequence[:]
        get_std_dev(self.int_sequence)
        assert self.int_sequence == old_sequence

    def test_get_stats_does_not_modify_sequence(self):
        self.int_sequence.reverse()
        old_sequence = self.int_sequence[:]
        get_stats(self.int_sequence)
        assert self.int_sequence == old_sequence

    def test_min_gets_min(self):
        min_val = get_min(self.int_sequence)
        assert min_val == 1

    def test_max_gets_max(self):
        max_val = get_max(self.int_sequence)
        assert max_val == 6
        
if __name__ == "__main__":
    unittest.main()
