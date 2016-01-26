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
        path = './/text'
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


    def check_for_long_left_column_lines(self, left, right, lcells, rcells):
        i = 0
        for line in lcells:
            length_in_words = len(line.split())
            if length_in_words > 3:
                common_terms = ['Size', 'Geographic locations', 'Inclusive dates', 'Bulk dates', 'Languages', 'Summary', 'Source', 'Related collection', 'Copyright', 'Citation']
                head = line.split()
                head = ' '.join(head[:2]) # first three words...
                for term in common_terms:
                    first_word_of_term = term.split()[0]
                    
                    if term.lower() in head.lower():
                        
                        length = len(term.split()) 
                        lcells[i] = ' '.join(line[: length])
                        rcells.insert(i, ' '.join(line[length:]))

                    elif first_word_of_term in head.lower():
                        lcells[i] = ' '.join(line[:1])
                        rcells.insert(i, ' '.join(line[1:]))

            i += 1
        return (lcells, rcells)
                # for term in 
    # def get_columnar_lines(self):
    #     columnar_lines = {}
    #     for top in self.lines_by_top:
    #         if len(self.lines_by_top[top]) > 1:
    #             columnar_lines[top] = self.lines_by_top[top]
    #     return columnar_lines

    def get_column_lefts(self):
        first  = (None, 0)
        second = (None, 0)

        for key,items in self.lines_by_left.iteritems():
            length = len(items)
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

        for line in self.lines_by_left[leftpos]:
            top = line.get('top')
            tops_list.append(top)
            by_tops[top] = line

        sorted(tops_list, reverse=True)

        text = ''
        for top in tops_list:
            text_value = etree.tostring(by_tops[top], method='text', encoding="UTF-8").strip()
            text += text_value
            only_whitespace = re.match('^\s*$', text_value)
            if only_whitespace:
                cells.append(text)
                text = ''
        return cells

    def checkForSummary(self, left_cells):
        prune = False
        i = 0
        for cell in left_cells:
            if 'summary' in cell.lower():
                prune = True
                break
            i += 1
        if prune == True:
            left_cells = left_cells[i+1:]
        return left_cells

    def remove_empty_string_list_items(self, cluttered):
        clean = []
        for item in cluttered:
            if item != '':
                clean.append(item)
        return clean

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
        
        if len(left_cells) > len(right_cells):
            left_cells = instance.checkForSummary(left_cells)

        left_cells = instance.remove_empty_string_list_items(left_cells)
        right_cells = instance.remove_empty_string_list_items(right_cells)

        left_cells, right_cells = instance.check_for_long_left_column_lines(left[0], right[0], left_cells, right_cells)

        table = {}
        i = 0

        for cell in left_cells:
            if i > len(right_cells) - 1:
                table[cell.strip()] = ''
            else:
                table[cell.strip()] = right_cells[i].strip()
            i += 1
        for key, value in table.iteritems():
            pass
        return table
