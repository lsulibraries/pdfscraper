#!/usr/bin/env python2.7

import unittest
from Logger import Logger
import os

class TestLoggerMethods(unittest.TestCase):

    def setUp(self):
        self.path = 'logtest'
        self.l = Logger(self.path)

    def tearDown(self):
        os.remove(self.path)

    def getlogContents(self):
        f = open(self.path, 'r')
        contents = f.read()
        f.close()
        return contents

    def test_add(self):
        self.l.add('hello')
        self.l.add('hello')
        contents = self.getlogContents()
        self.assertEquals(contents, 'hello\nhello\n')        
        



if __name__ == '__main__':
    unittest.main()