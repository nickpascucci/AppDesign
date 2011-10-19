#! /usr/bin/env python

"""Unit tests for the cached urlopen."""

import sqlite3
import unittest
import cache

__author__ = "Nick Pascucci (npascut1@gmail.com)"


class MyTest(unittest.TestCase):
    def setUp(self):
        self.cache = cache.Cache('test.db')

        self.connection = sqlite3.connect('test.db')
        self.cursor = self.connection.cursor()
        self.generate_database()

    def tearDown(self):
        self.connection.close()

    def generate_database(self):
        self.cursor.execute('DROP TABLE cache;');
        self.cursor.execute('CREATE TABLE cache(name TEXT, last_access INTEGER, '
                            'retrieved_data BLOB);')
        self.cursor.execute('INSERT INTO cache VALUES ("test.com", 1000, '
                            '"<html><b>Foo</b></html>");')
        self.cursor.execute('INSERT INTO cache VALUES ("test1.com", 1200, '
                            '"<html><b>Bar</b></html>");')
        self.cursor.execute('INSERT INTO cache VALUES ("test2.com", 1400, '
                            '"<html><b>Baz</b></html>");')
        self.connection.commit()

    def test_check_cache(self):
        assert self.cache.check("test.com")
        assert not self.cache.check("failtest.com")

    def test_free_space_in_cache(self):
        assert self.cache.check("test.com")
        self.cache.cull()
        assert not self.cache.check("test.com")

    def test_add_to_cache(self):
        assert not self.cache.check("test3.com")
        self.cache.add("test3.com", "<html><b>Quux</b></html>")
        assert self.cache.check("test3.com")

    def test_add_to_cache_makes_space(self):
        self.cache.maxsize = 1
        assert self.cache.size() == 1
        assert self.cache.check("test2.com")
        self.cache.add("test.com", "<html><b>Foo</b></html>")
        assert self.cache.size() == 1
        assert self.cache.check("test.com")
        assert not self.cache.check("test2.com")
        
    def test_cache_size(self):
        assert self.cache.size() == 3

    def test_get_cached_data(self):
        html = self.cache.get("test.com")
        assert html == "<html><b>Foo</b></html>"

    def test_get_cached_updates_timestamp(self):
        self.cursor.execute("SELECT last_access FROM cache WHERE name=?;",
                            ("test.com",))
        result = self.cursor.fetchone()[0]
        self.cache.get("test.com")
        self.cursor.execute("SELECT last_access FROM cache WHERE name=?;",
                            ("test.com",))
        updated_result = self.cursor.fetchone()[0]
        assert updated_result > result


if __name__ == "__main__":
   unittest.main()
