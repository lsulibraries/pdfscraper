#!/usr/bin/env python2.7

import time

class Logger():

    severity_map = {
            'd': (1, 'DEBUG'),
            'i': (2, 'INFO'),
            'm': (3, 'MISSING'),
            'j': (4, 'JU_mapNKY'),
            'e': (5, 'ERROR')
        }
    severity = 2

    def __init__(self, logfile_path, severity='i'):
        self.file_handle = open(logfile_path, 'a')
        self.severity = self.severity_map[severity][0]

    def add(self, msg, sev='i'):
        if self.severity_map[sev][0] >= self.severity:
            date = time.strftime("%H:%M:%S")
            entry = '{} [{}] {}\n'.format(date, self.severity_map[sev][1], msg)
            self.file_handle.write(entry)
            self.file_handle.flush()

    def close(self):
        self.file_handle.close()