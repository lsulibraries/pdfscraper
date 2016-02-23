#!/usr/bin/env python2.7

import unittest
from Logger import Logger
import os
import time


class TestLoggerMethods(unittest.TestCase):

    def setUp(self):
        self.path = 'logtest'

    def tearDown(self):
        os.remove(self.path)

    def getlogContents(self):
        f = open(self.path, 'r')
        contents = f.read()
        f.close()
        return contents

    def test_add(self):
        l = Logger(self.path, 'i')
        l.add('hello')
        date1 = time.strftime("%H:%M:%S")
        l.add('hello')
        date2 = time.strftime("%H:%M:%S")
        contents = self.getlogContents()
        self.assertEquals(contents, '{} [INFO] hello\n{} [INFO] hello\n'.format(date1, date2))

    def test_add_with_severity(self):
        localLogger = Logger(self.path, 'm')
        localLogger.add('hello')
        localLogger.add('hello', 'm')
        date2 = time.strftime("%H:%M:%S")
        contents = self.getlogContents()
        self.assertEquals(contents, '{} [{}] hello\n'.format(date2, localLogger.severity_map['m'][1]))

if __name__ == '__main__':
    unittest.main()
