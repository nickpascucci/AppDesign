#! /usr/bin/env python
"""A simplistic statistical calculator."""

# Enable floating point division by default.
from __future__ import division
import math

__author__ = "Nick Pascucci (npascut1@gmail.com)"

def get_avg(seq):
    """Calculate the average of a sequence of numbers.

    Args:
    seq - A sequence of numbers.

    Returns:
    The average value.
    """
    tot = sum(seq)
    return tot/len(seq)

def get_std_dev(seq, avg=None):
    """Calculate the standard deviation of a sequence of numbers.

    Args:
    seq - A sequence of numbers.
    avg - The average value of the sequence, if precomputed. If None, the
    average will be computed automatically.

    Returns:
    The standard deviation for the sequence.
    """
    if not avg:
        avg = get_avg(seq)
    squares = 0
    for i in seq:
        dist = i - avg
        squares += dist ** 2
    squares_avg = squares/len(seq)
    std_dev = math.sqrt(squares_avg)
    return std_dev

def get_stats(values):
    """Calculate statistics for the given sequence.
    Args:
    values - A sequence of numerical types.

    Returns:
    A tuple (min, max, avg, std_dev).
    """
    seq = values[:]
    seq.sort()
    stats = (
        seq[0],  # Minimum
        seq[-1],  # Maximum
        get_avg(seq),  # Average
        get_std_dev(seq)  # Std. Deviation
        )
    return stats

def main():
    vals = []
    print ("Welcome to the statistical calculator.\n"
           "Enter any number of numbers.\n"
           "When you're done, enter a non-numerical character to calculate.")

    try:
        while True:
            num = float(raw_input(""))
            vals.append(num)
    except ValueError:
        # User input a non-float value. We'll just start the calculation.
        pass

    print "All right, calculating!"
    stats = get_stats(vals)
    print ("Minimum: %f\n"
           "Average: %f\n"
           "Maximum: %f\n"
           "Standard Deviation: %f\n") % stats

if __name__ == "__main__":
    main()
