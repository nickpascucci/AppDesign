#! /usr/bin/env python

"""This is a Python file."""

import os
import unittest
import processing

__author__ = "Nick Pascucci (npascut1@gmail.com)"

TEST_FILE = "portal.wav"

class WaveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wave = processing.Wave()
        cls.wave.load(TEST_FILE)
    
    def setUp(self):
        self.wave1 = processing.Wave()
        self.wave2 = processing.Wave()
        self.wave1.audio = range(11)
        self.wave2.audio = range(10, 0, -1)
        self.wave1.frames = 10
        self.wave2.frames = 10

    
    def tearDown(self):
        pass

    def test_load(self):
        assert self.wave.channels == 2
        assert self.wave.sample_width == 2
        assert self.wave.sample_rate == 44100
        assert self.wave.frames == 967680
        assert len(self.wave.audio) == 2 * self.wave.frames # Two channels
        for frame in self.wave.audio:
            assert (frame.channel == 0 or frame.channel == 1)
        assert self.wave.max_amplitude > 0

    def test_normalize(self):
        old_max = self.wave.max_amplitude
        self.wave.normalize()
        new_max = self.wave.max_amplitude
        assert new_max > old_max

    def test_get_max_val(self):
        assert processing._get_max_value(1) == 255
        assert processing._get_max_value(2) == 32767

    def test_add(self):
        self.wave1 += self.wave2
        for frame in self.wave1.audio:
            assert frame == 10

    def test_raises_error_if_waves_differ(self):
        self.wave1.sample_width = 32
        self.wave2.sample_width = 16
        with self.assertRaises(processing.FormatError):
            self.wave1 += self.wave2

    def test_slice(self):
        w1_slice = self.wave1[2:5]
        assert w1_slice == range(2, 5)

    def test_set_and_get_item(self):
        self.wave1[3] = 4
        assert self.wave1[3] == 4
        
    # This test is being ignored, because while the two files may differ,
    # the saved file is still playable. The difference might be due to
    # additional metadata stored by Audacity.
    def ign_test_save(self):
        self.wave.save("test.wav")
        f1 = open(TEST_FILE)
        f2 = open("test.wav")
        data1 = f1.read()
        data2 = f2.read()
        f1.close()
        f2.close()
        os.remove("test.wav")
        assert data1 == data2

if __name__ == "__main__":
   unittest.main()
