#! /usr/bin/env python

"""A cached nameopen implementation.."""

import time
import sqlite3
import urllib

__author__ = "Nick Pascucci (npascut1@gmail.com)"

class CachedData(object):
    """Super simple class to store cached results in a file-like object."""
    def __init__(self, data):
        self.data = data

    def read(self):
        """Read the data stored in the object."""
        return self.data

class Cache(object):
    """A cache for frequently accessed binary blobs.

    This cache stores the last access time of its entries, and uses a least
    recently used replacement policy. The maximum size of the cache can be set
    with the maxsize attribute, and will be enforced immediately. Any binary
    blob can be stored in the cache within the limitations of the backing sqlite
    database.
    """
    def __init__(self, path='cache.db', maxsize=5):
        """Create a new cache.

        Creates a sqlite3 database file if one does not exist at the given path.

        @param path The file containing the database.
        @param maxsize The maximum size of the cache.
        """
        self._db_conn = sqlite3.connect(path)
        self._cursor = self._db_conn.cursor()
        self._setup()
        self._maxsize = 0
        # Setting maxsize via property lets us take advantage of auto-culling if
        # the cache is already set up and larger than allowed.
        self.maxsize = maxsize
        self.missed = 0
        self.hit = 0

    def set_max_size(self, val):
        """Set the maximum size of the cache and cull it.

        @param val The maximum size of the cache.
        """
        self._maxsize = val
        while self.size() > self._maxsize:
            self.cull()

    def get_max_size(self):
        """Get the maximum size of the cache.

        @return The maximum size.
        """
        return self._maxsize

    maxsize = property(get_max_size, set_max_size)

    def _setup(self):
        """Create a new table if needed."""
        self._cursor.execute("SELECT name FROM sqlite_master "
                             "WHERE type='table';")
        existing_tables = self._cursor.fetchone()
        if not "cache" in existing_tables:
            self._cursor.execute("CREATE TABLE cache (name TEXT, "
                                 "last_access INTEGER, retrieved_data BLOB);")
            self._db_conn.commit()

    def open(self, name):
        """Open the given NAME, first attempting to retrieve cached data.

        @param name The NAME to retrieve.
        @return The HTML data at that NAME.
        """
        if self.check(name):
            self.hit += 1
            return self.get(name)
        else:
            self.missed += 1
            data = urllib.urlopen(name)
            self.add(name, data.read())
            return data

    def check(self, name):
        """Check the cache for cached data associated with name.

        @param name The address to check.
        @return True if the address is cached, false if not.
        """
        self._cursor.execute("SELECT name FROM cache WHERE name=?;", (name,))
        result = self._cursor.fetchone()
        return bool(result)

    def get(self, name):
        """Get the cached data for the NAME.

        @param name The identifier for the data.
        @return The data from the last time it was cached.
        """
        self._cursor.execute("SELECT retrieved_data FROM cache WHERE name=?;",
                             (name,))
        data = self._cursor.fetchone()[0]
        self._cursor.execute("UPDATE cache SET last_access=? WHERE name=?;",
                             (time.ctime(), name))
        self._db_conn.commit()
        return data

    def cull(self):
        """Remove the least-recently accessed item from the cache."""
        self._cursor.execute("SELECT name FROM cache ORDER BY last_access ASC;")
        result = self._cursor.fetchone()
        self._cursor.execute("DELETE FROM cache WHERE name=?;", result)
        self._db_conn.commit()

    def add(self, name, data):
        """Add an item to the cache.

        @param name The identifer for the data.
        @param data The data to cache.
        """
        if self._maxsize == self.size():
            self.cull()
        self._cursor.execute("INSERT INTO cache VALUES (?, ?, ?);",
                             (name, time.ctime(), data))
        self._db_conn.commit()

    def stats(self):
        """Generate statistics for the cache.

        @return A tuple (missed, hit).
        """
        return (self.missed, self.hit)

    def size(self):
        """Check the size of the cache.

        @return The number of cache entries.
        """
        self._cursor.execute("SELECT * FROM cache;")
        return len(self._cursor.fetchall())

    def __del__(self):
        self._db_conn.close()
