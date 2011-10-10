#! /usr/bin/env python

"""Unit tests for user bookmark storage."""

__author__ = "Nick Pascucci (npascut1@gmail.com)"

import os
import unittest
import bookmark_store as bstore

class BookmarkStoreTest(unittest.TestCase):
    def setUp(self):
        self.store = bstore.BookmarkStore()
        self.test_string = ('<DT><A HREF="http://www.gnu.org" '
                       'ADD_DATE="1271308716">GNU</A></DT>')
        self.test_html = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL>
    <DT><A HREF="http://www.gnu.org" ADD_DATE="1271308716">GNU</A></DT>
</DL>"""

    def tearDown(self):
        pass

    def test_import_bookmarks_from_string(self):
        self.store.import_from_string(self.test_string)
        assert "GNU" in self.store

    def test_get_bookmarks_easy(self):
        matches = bstore._get_bookmarks(self.test_string)
        assert matches == [self.test_string]

    def test_get_bookmarks_hard(self):
        matches = bstore._get_bookmarks("asdflkjasdlfkjasdflkjxcm.,>ASDF><''" +
                                        self.test_string +
                                        "asdflkjasf;lkjasfd;lkj")
        assert matches == [self.test_string]

    def test_import_from_file(self):
        test_file = open("test_bookmarks.html", "r")
        self.store.import_from_file(test_file)
        assert "GNU" in self.store
        assert "Kernel.org" in self.store
        gnu = self.store["GNU"]
        assert gnu.url == "http://www.gnu.org"

    def test_export_to_string(self):
        self.store.import_from_string(self.test_string)
        html = self.store.export_to_string()
        assert html == self.test_html

    def test_export_to_file(self):
        self.store.import_from_string(self.test_string)
        self.store.export_to_file("testoutput.html")
        outfile = open("testoutput.html", "r")
        text = outfile.read()
        outfile.close()
        os.remove("testoutput.html")
        assert text == self.test_html
        

if __name__ == "__main__":
    unittest.main()
