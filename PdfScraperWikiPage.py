#! /usr/bin/env python2.7
from lxml import etree
import re

class PdfScraperWikiPage():

    tables = []
    paras  = []
    chunks = []
    lines_by_top   = {}
    lines_by_left  = {}

    def __init__(self, tree):
        self.tree = tree
        lines_gotten = self.get_lines()
        self.lines_by_left = lines_gotten[0]
        self.lines_by_top  = lines_gotten[1]


    def get_lines(self):
        print(self.tree)
        path = '//text'
        lines = self.tree.xpath(path)
        lefts = {}
        tops  = {}
        for line in lines:
            top  = line.get('top')
            left = line.get('left')
            if (top is not None) and (top not in tops):
                tops[top] = []
            tops[top].append(line)

            if (left is not None) and (left not in lefts):
                lefts[left] = []
            lefts[left].append(line)
        return (lefts, tops)

    def get_columnar_lines(self):
        columnar_lines = {}
        for top in self.lines_by_top:
            if len(self.lines_by_top[top]) > 1:
                columnar_lines[top] = self.lines_by_top[top]
        return columnar_lines

    def get_column_lefts(self):
        first  = (None, 0)
        second = (None, 0)

        for key,items in self.lines_by_left.iteritems():
            length = len(items)
            # print 'pos {} has {} items'.format(key, length)
            if length > first[1]:
                second = first
                first = (key, length)
            elif length > second[1]:
                second = (key, length)
        return (first, second)

    def get_col_cells(self, leftpos):
        tops_list = []
        by_tops   = {}
        cells = []
        # print leftpos
        # print self.lines_by_left[leftpos]

        for line in self.lines_by_left[leftpos]:
            top = line.get('top')
            tops_list.append(top)
            by_tops[top] = line

        sorted(tops_list, reverse=True)

        text = ''
        for top in tops_list:
            text_value = etree.tostring(by_tops[top], method='text').strip()
            text += text_value
            only_whitespace = re.match('^\s*$', text_value)
            if only_whitespace:
                cells.append(text)
                text = ''
        return cells

    @staticmethod
    def get_table(tree):
        instance = PdfScraperWikiPage(tree)
        cols = instance.get_column_lefts()
        one, two = cols
        if one[0] > two[0]:
            left = two
            right = one
        else:
            left = one
            right = two

        left_cells = instance.get_col_cells(left[0])
        right_cells = instance.get_col_cells(right[0])

        table = {}
        i = 0
        for cell in left_cells:
            table[cell.strip()] = right_cells[i].strip()
            i += 1
        return table
