#! /usr/bin/env python2

import lxml.etree as ET


class ReadSummary():
    def __init__(self, element_tree):
        self.element_tree = element_tree
        header = 'Size'
        self.get_text_after_keywork(header)

    def get_text_after_keywork(self, header):
        beginning_page = '3'
        elem_of_header = self.element_tree.xpath(
            '//page[@number="{}"]/text/b[text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{}")]]'.format(
                beginning_page, header.lower().strip().replace('.', '')))
        all_possible_headers = ('size', 'geographic', 'geographic locations', 'inclusive dates' 'inclusive', 'bulk', 'bulk dates', 'languages', 'summary', 'restrictions on access', 'restrictions', 'access', 'copyright', 'citation', 'stack', 'stack location')
        text_after_keyword = []
        for i in self.get_siblings_and_children(elem_of_header):
            for possible_header in all_possible_headers:
                if possible_header != header:
                    if i.lower().strip().replace('.', '') == possible_header.lower().strip().replace('.', ''):
                        continue
            text_after_keyword.append(i.strip())
        print('{}: {}\n'.format(header, text_after_keyword))

    def get_siblings_and_children(self, elem_of_header):
        list_of_sibling_children_text = []
        if len(elem_of_header) < 1:
            return list_of_sibling_children_text
        elems_following = elem_of_header[0].getparent().itersiblings()
        for sibling in elems_following:
            sibling_str = ET.tostring(sibling, encoding="utf-8", method='text', ).strip()
            if sibling_str and len(sibling_str) > 0:
                list_of_sibling_children_text.append(sibling_str)
        return list_of_sibling_children_text


if __name__ == '__main__':
    filename = 'findaid_list.txt'
    uids_wo_summary = ('3070', '4644')
    with open(filename, 'r') as f:
        for uid in f.readlines():
            if uid.strip() in uids_wo_summary:
                print(uid)
                continue
            uid = uid.strip()
            element_tree = ET.parse('starting_xmls/SummaryPageElem/{}.xml'.format(uid))
            print(uid)
            ReadSummary(element_tree)
