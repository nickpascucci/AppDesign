"""Objects for easy bookmark storage."""

__author__ = "Nick Pascucci (npascut1@gmail.com)"

import datetime

class Bookmark(object):
    """Representation of a user bookmark."""
    def __init__(self, name, address, timestamp):
        self.name = name
        self.url = address
        self.timestamp = int(timestamp)
        dt = datetime.datetime.fromtimestamp(self.timestamp)
        self.date = dt.strftime("%Y-%m-%d-%H-%M")

    def __str__(self):
        return "%(name)s: %(url)s\tCreated: %(date)s" % self.__dict__
        
    def to_link(self):
        """Convert this bookmark to an HTML link."""
        return ('<A HREF="%(url)s" '
                'ADD_DATE="%(timestamp)s">%(name)s</A>') % self.__dict__
