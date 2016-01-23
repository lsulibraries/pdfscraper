#!/usr/bin/env python2.7

class ReadNSV:

    def __init__(self, path):
        self.file = path

    def getLines(self):
        print 'hello'
        f = open(self.file, 'r')
        lines = []
        for line in f:
            lines.append(line.strip())
        f.close()
        return lines
