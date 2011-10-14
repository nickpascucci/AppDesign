#! /usr/bin/env python

"""Download images from the web."""

import os.path
import re
import sys
import urllib

__author__ = "Nick Pascucci (npascut1@gmail.com)"

IMAGE_RE = r'(?<=src=")[a-zA-Z0-9.\-_&@#$\*\(\)\[\]:/]*'
image_matcher = re.compile(IMAGE_RE)

EXTENSION_RE = r'.*(.png|.PNG|.jpg|.JPG|.svg|.SVG|.gif|.GIF)$'
extension_matcher = re.compile(EXTENSION_RE)

SITENAME_RE = r'^http://.*?(?=/)'
sitename_matcher = re.compile(SITENAME_RE)

def get_image_paths(html):
    """Extract image paths from the given html.

    @param html The raw html to analyze.
    @return A list of image paths.
    """
    matches = [m.group(0) for m in image_matcher.finditer(html)
               if match_extension(m.group(0))]
    return matches

def match_extension(path):
    """Determine if the path is an image.

    @param path A potential image path.
    @return True if the path ends with an image extension.
    """
    return bool(extension_matcher.match(path))

def images_from_url(url):
    """Retrieve a list of image paths from the given URL.

    @param url The target URL to retrieve.
    @return A list of the image paths.
    """
    filehandle = urllib.urlopen(url)
    html = filehandle.read()
    images = get_image_paths(html)
    return images

def sitename(url):
    """Extract the sitename component from the given URL.

    @param url The url to truncate.
    @return The site's root URL.
    """
    return sitename_matcher.match(url).group(0)

def download_image(url, path):
    """Download an image from the given url under path.

    @param url The url to download from.
    @param path The path to download.
    """
    full_path = ""
    if path.startswith("http"):
        full_path = path
    elif path.startswith("/"):
        full_path = sitename(url) + path
    else:
        full_path = url + "/" + path
    if full_path:
        print "\tDownloading from", full_path
        urllib.urlretrieve(full_path, os.path.basename(path))

def download_images(url):
    """Download all images from the given url.

    @param url The target URL.
    """
    images = images_from_url(url)
    for image in images:
        print "Downloading", image
        download_image(url, image)

def main():
    if len(sys.argv) != 2:
        print "Usage: download.py <url>"
    download_images(sys.argv[1])

if __name__ == "__main__":
   main()
