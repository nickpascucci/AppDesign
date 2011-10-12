#! /usr/bin/env python

"""Audio filters to apply to waveforms."""

__author__ = "Nick Pascucci (npascut1@gmail.com)"

from processing import frame

def add_echo(wave, delay, decay_factor):
    new_wave = wave.copy()
    for i in range(delay, len(wave)):
        new_wave[i] = frame(amplitude=wave[i-delay].amplitude * decay_factor,
                            channel=new_wave[i].channel)
    return new_wave

def chipmunkify(wave, degree):
    new_wave = wave.copy()
    count = -1
    new_wave.audio = [frame for index, frame
                      in enumerate(new_wave)
                      if not (index % degree == 0)]
    return new_wave
