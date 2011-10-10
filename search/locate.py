#! /usr/bin/env python

"""Locate files using fuzzy matching."""
from __future__ import division
import os.path
import sys

def locate(filename, start):
    """Search the filesystem under start for filename.

    @param filename: The filename to look for.
    @param start: The starting directory.
    @return: A list of matching names, ordered from best to worst.
    """
    results = []
    os.path.walk(start, visit, (results, filename))
    results.sort(reverse=True)
    if results[0][0] == 1:
        results = [path for rating, path in results if rating == 1]
    else:
        results = [path for rating, path in results if rating > 0]
    return results
    
def visit(tools, dirname, names):
    """Examine the contents of a directory, rate them, and add them to results.

    @param tools: A tuple (results, filename) with the results list to store
    into and the target filename.
    @param dirname: The current directory name.
    @param names: The names of the files in the current directory.
    """
    results, filename = tools
    for name in names:
        rating = rate(name, filename)
        results.append((rating, os.path.join(dirname, name)))

def rate(name, filename):
    """Rate the closeness of two filenames.

    @param name: The name of the first file.
    @param filename: The name of the second file.
    @return: A float between 0.0 and 1.0, with greater values indicating a
    closer match.
    """
    rating = 0
    if name == filename:
        rating = 1
    elif filename in name:
        # Rating is influenced by the difference in length between two strings.
        rating += 0.5 + (0.5 - (0.5 * abs(len(name) - len(filename))/len(name)))
    return rating

def main():
    if len(sys.argv) != 3:
        print """Usage: ./locate.py <filename> <directory>"""
        exit(1)
    filename = sys.argv[1]
    start = sys.argv[2]
    results = locate(filename, start)
    for result in results[:5]:
        print result

if __name__ == "__main__":
    main()
