#!/usr/bin/env python2.7

from ReadNSV import ReadNSV
import unittest

class TestReadNSVMethods(unittest.TestCase):

    def testGetLines(self):
        nsv = ReadNSV('testList.nsv')
        self.assertEquals(len(nsv.getLines()), 5)

if __name__ == '__main__':
    unittest.main()