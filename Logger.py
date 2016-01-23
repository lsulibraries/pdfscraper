#!/usr/bin/env python2.7

class Logger():

    def __init__(self, logfile_path):
        self.file_handle = open(logfile_path, 'a')


    def add(self, msg):
        self.file_handle.write(msg + '\n')
        self.file_handle.flush()

    def close(self):
        self.file_handle.close()