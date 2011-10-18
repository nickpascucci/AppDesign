#! /usr/bin/env python

"""Unit tests for the image downloader."""

import unittest
import download

__author__ = "Nick Pascucci (npascut1@gmail.com)"


class DownloadTest(unittest.TestCase):
   def setUp(self):
       pass

   def tearDown(self):
       pass

   def test_img_matcher(self):
       html = """<html>
<body>
<b>Hi there!</b>
<img src="abcd-(myfile)[1].jpg">
</body>
</html>
"""
       paths = download.get_image_paths(html)
       assert paths == ["abcd-(myfile)[1].jpg"]
       
   def test_img_matcher_http(self):
       html = """<html>
<body>
<b>Hi there!</b>
<img src="http://www.def.com/abcd-(myfile)[1].jpg">
</body>
</html>
"""
       paths = download.get_image_paths(html)
       assert paths == ["http://www.def.com/abcd-(myfile)[1].jpg"]

   def test_extension_matcher(self):
       filename = "abcdef.jpg"
       assert download.match_extension(filename)
       filename = "abcdef.txt"
       assert not download.match_extension(filename)

   def test_sitename_matcher(self):
       site = "http://www.xkcd.com/208/"
       sitename = download.sitename(site)
       assert "http://www.xkcd.com" == sitename       
       
if __name__ == "__main__":
   unittest.main()
