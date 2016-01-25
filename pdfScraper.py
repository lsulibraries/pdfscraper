#!/usr/bin/env python2.7

import os
import re
# import urllib2

import scraperwiki
# from lxml.builder import E
from lxml import etree
import xml.etree.ElementTree as ET

from ReadNSV import ReadNSV
from Logger import Logger as L
from terms_dict_set import get_term_set_dict


class FindingAidPDFtoEAD():
    def __init__(self, url, logger=None):
        if logger is None:
            logger = L('log'.format(url))
        self.url = url
        self.logger = logger
        self.element_tree = self.read_url_return_etree(self.url)

    def log(self, msg, sev='i'):
        self.logger.add('{}:   {} '.format(self.url, msg), sev)

    def read_url_return_etree(self, url):
        '''normal 'pull pdf from web and interpret' code'''
        # self.pdfdata = urllib2.urlopen(url).read()   # Necessary code for pulling pdf from web.
        # self.xmldata = scraperwiki.pdftoxml(self.pdfdata)
        # self.xmldata = bytes(bytearray(self.xmldata, encoding='utf-8'))
        # self.element_tree = etree.fromstring(self.xmldata)

        '''temporary 'read cached file from harddrive' monkeypatch'''
        with open('cached_pdfs/' + self.url[-8:], 'r') as f:
            self.pdfdata = f.read()
            self.xmldata = scraperwiki.pdftoxml(self.pdfdata)
            self.xmldata = bytes(bytearray(self.xmldata, encoding='utf-8'))
            self.element_tree = etree.fromstring(self.xmldata)
        self.log('opened file', 'm')
        return self.element_tree

    def run_conversion(self):
        # print etree.tostring(self.element_tree, pretty_print=True)  # dev only
        # self.print_xml_to_file()                                    # dev only
        contents_of_inventory = self.grab_contents_of_inventory()
        self.c_o_i_ordered = sorted(contents_of_inventory, key=lambda item: int(item[1][0]))
        print 'COI: ', self.c_o_i_ordered
        compiled_ead = self.get_ead()
        self.print_ead_to_file(compiled_ead)

    def grab_contents_of_inventory(self):
        contents = self.element_tree.xpath('//page/text[b[contains(text(), "CONTENTS OF INVENTORY")]]/following-sibling::text/a')
        pruned_elem_list = self.remove_non_text_elements(contents)
        if re.findall('[a-zA-Z]', etree.tostring(pruned_elem_list[0], method='text')) and re.findall('[0-9]', etree.tostring(pruned_elem_list[0], method='text')):
            top_header_page_dict = self.collapse(contents)
            inventory = []
            for top, header_page in top_header_page_dict.iteritems():
                header, page = re.findall('([A-Z\s\/a-z]+)[\s\.]+([0-9\-]+)', header_page)[0]
                pages_tuple = self.split_on_char('-', page)
                temp_page_start, temp_page_end = pages_tuple
                temp_page_start, temp_page_end = int(temp_page_start), int(temp_page_end)
                pages_tuple = (temp_page_start, temp_page_end)
                inventory.append((header, pages_tuple))
        else:
            pruned_elem_list = self.join_disjointed_header_page(pruned_elem_list)
            inventory = []
            for elem in pruned_elem_list:
                if re.findall('([A-Z\s\/a-z]+)[\s\.]+([0-9\-]+)', elem):
                    header, page = re.findall('([A-Z\s\/a-z]+)[\s\.]+([0-9\-]+)', elem)[0]
                    # Here need to be a way of parsing 4452.pdf Appendices
                    pages_tuple = self.split_on_char('-', page)
                    temp_page_start, temp_page_end = pages_tuple
                    temp_page_start, temp_page_end = int(temp_page_start), int(temp_page_end)
                    pages_tuple = (temp_page_start, temp_page_end)
                    inventory.append((header, pages_tuple))
        return inventory

    def remove_non_text_elements(self, elem_list):
        elements_with_text = []
        for pos, item in enumerate(elem_list):
            if re.findall('([A-Za-z0-9]+)', etree.tostring(item, method='text')):
                elements_with_text.append(item)
        return elements_with_text

    def collapse(self, elem_list):
        collapsed = {}
        for elm in elem_list:
            top = elm.getparent().get('top')
            if top in collapsed:
                existing_text = collapsed[top] + ' ' + etree.tostring(elm, method='text').strip().lower()
            else:
                collapsed[top] = '' + etree.tostring(elm, method='text').strip().lower()
        return collapsed

    def join_disjointed_header_page(self, elem_list):
        num_of_elems = len(elem_list)
        joined_elem_list = []
        for i in xrange(num_of_elems/2):
            header, page = elem_list[2*i], elem_list[(2*i)+1]
            head_page_str = "{} {}".format(etree.tostring(header, method='text'), etree.tostring(page, method='text'))
            joined_elem_list.append(head_page_str)
        return joined_elem_list

    def split_on_char(self, char, text):
        if char in text:
            start, end = text.split(char)
        else:
            start, end = text, text
        return (start, end)

    def convert_text_after_header_to_string(self, header_snippet):
        for pos, i in enumerate(self.c_o_i_ordered):
            if header_snippet.lower() in i[0].lower():
                if pos == len(self.c_o_i_ordered)-1:
                    return ' '.join(self.get_text_after_header(i)).decode("utf8")
                else:
                    return ' '.join(self.get_text_after_header(i, self.c_o_i_ordered[pos+1])).decode("utf8")

    def get_text_after_header(self, inventory_item, following_inventory_item=None):
        header, (beginning_page, end_page) = inventory_item
        elem_of_header = self.element_tree.xpath('//page[@number="{}"]/text/b[text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{}")]]'.format(beginning_page, header.lower().strip()))
        text_after_header = []
        for i in self.get_first_page_siblings_and_children(elem_of_header):
            text_after_header.append(i.strip())
        if following_inventory_item:
            following_header, (following_beginning_page, following_end_page) = following_inventory_item
            if following_beginning_page - beginning_page > 1:
                for page in xrange(beginning_page+1, following_beginning_page):
                    self.get_middle_page_siblings_and_childrent(page)
                    text_after_header.append(i.strip())
            if self.get_last_page_siblings_and_children(following_header, following_beginning_page):
                for i in self.get_last_page_siblings_and_children(following_header, following_beginning_page):
                    text_after_header.append(i.strip())
        else:
            for i in self.do_get_last_pages_if_last_header(beginning_page):
                text_after_header.append(i.strip())
        if len(text_after_header) > 1:
            self.log('Got {} lines afer header {}'.format(len(text_after_header), header))
        return text_after_header

    def get_first_page_siblings_and_children(self, elem_of_header):
        list_of_sibling_children_text = []
        if len(elem_of_header) < 1:
            return list_of_sibling_children_text
        elems_following = elem_of_header[0].getparent().itersiblings()
        for sibling in elems_following:
            sibling_str = self.get_text_recursive(sibling)
            if sibling_str and len(sibling_str) > 0:
                list_of_sibling_children_text.append(sibling_str)
        return list_of_sibling_children_text

    def get_middle_page_siblings_and_childrent(self, page):
        list_of_sibling_children_text = []
        elems_following = self.element_tree.xpath('//page[@number="{}"]/text'.format(page))
        for sibling in elems_following:
            sibling_str = self.get_text_recursive(sibling)
            if sibling_str and len(sibling_str) > 0:
                list_of_sibling_children_text.append(sibling_str)
        return list_of_sibling_children_text

    def get_last_page_siblings_and_children(self, end_header, end_page):
        header_xpath = self.element_tree.xpath('//page[@number="{}"]/text/b[text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{}")]]'.format(end_page, end_header.lower().strip()))
        list_of_sibling_children_text = []
        elems_preceding = header_xpath[0].getparent().itersiblings(preceding=True)
        for sibling in elems_preceding:
            sibling_str = self.get_text_recursive(sibling)
            if sibling_str and len(sibling_str) > 0:
                list_of_sibling_children_text.append(sibling_str)
        list_of_sibling_children_text = list_of_sibling_children_text.reverse()
        return list_of_sibling_children_text

    def do_get_last_pages_if_last_header(self, beginning_page):
        temp_text_list = []
        count = 0
        while (self.get_pdf_length() - beginning_page) - count > 0:
            temp_text_list.append(self.get_middle_page_siblings_and_childrent(beginning_page + 1 + count))
            count += 1
        return temp_text_list

    def get_pdf_length(self):
        list_of_all_page_nums = [int(i) for i in self.element_tree.xpath('//page/@number')]
        return max(list_of_all_page_nums)

    def get_text_recursive(self, element):
        return etree.tostring(element, method='text', encoding="UTF-8").strip()

    # def log_if_missing(self, element, xpath_result_len, message=''):
    #     self.log('xpath failed to find title', 'm')

    def get_ead(self):
        ead = ET.Element('ead', attrib={'relatedencoding': "MARC21", 'type': "inventory", 'level': "collection", })
        ead.append(self.get_eadheader())
        ead.append(self.get_archdesc())
        ''' some preface on all xmls like this:::::?
            <?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE ead PUBLIC "+//ISBN 1-931666-00-8//DTD ead.dtd (Encoded Archival Description (EAD) Version 2002)//EN" "../ead_dtd/ead.dtd">'''
        return ead

    def get_eadheader(self):
        el = ET.Element('eadheader')
        el.append(self.get_eadid())
        el.append(self.get_filedesc())
        return el

    def get_eadid(self):
        return ET.Element('eadid', attrib={'countrycode': 'us', 'url': self.url}, )

    def get_filedesc(self):
        el = ET.Element('filedesc')
        el.append(self.get_titlestmt())
        el.append(self.get_publicationstmt())
        return el

    def get_titlestmt(self):
        el = ET.Element('titlestmt')
        el.append(self.get_titleproper())
        el.append(self.get_subtitle())
        el.append(self.get_author())
        return el

    def get_titleproper(self):
        el = ET.Element('titleproper')
        el.text = self.extract_title()
        el.append(self.get_num())
        return el

    def extract_title(self):
        # titleproper - needs to account for multiple lines in some docs
        wholetitle = []
        titlelines = self.element_tree.xpath('//page[@number="1"]/text[@top>="200" and @width>"10"]/b')
        for el in titlelines:
            wholetitle.append(el.text.strip())
        return 'A GUIDE TO THE ' + ' '.join(wholetitle)

    def get_num(self):
        el = ET.Element('num', attrib={'type': 'Manuscript'})
        el.text = self.extract_mss()
        return el

    def extract_mss(self):
        titlelines = self.element_tree.xpath('//page[@number="1"]/text[@top>="200" and @width>"10"]/b')

        # figuring out what the top value of the last line of the title is
        titlelineend = titlelines[-1].getparent().get('top')

        # num - assume it is between 12 and 25 units below the last line of title
        #    (a better way might have been to take next text node)
        numlinenumberA = str(int(titlelineend) + 12)  # 347
        numlinenumberB = str(int(titlelineend) + 25)  # 360
        xpath_address = '//page[@number="1"]/text[@top>=' + numlinenumberA + ' and @top<=' + numlinenumberB + ']'
        mss_elem = self.element_tree.xpath(xpath_address)[0]
        return mss_elem.text

    def get_subtitle(self):
        el = ET.Element('subtitle')
        el.text = self.extract_subtitle()
        return el

    def extract_subtitle(self):
        return 'A Collection in the Louisiana and Lower Mississippi Valley Collections'

    def get_author(self):
        el = ET.Element('author')
        el.text = self.extract_author()
        return el

    def extract_author(self):
        try:
            pdfauthor = self.element_tree.xpath('//page[@number="1"]/text[text()[normalize-space(.)="Compiled by"]]')[0].getnext().text.strip()
        except:
            pdfauthor = 'Special Collections Staff'
        return pdfauthor

    def get_publicationstmt(self):
        el = ET.Element('publicationstmt')
        el.append(self.get_publisher())
        el.append(self.get_addressline())
        el.append(self.get_date())
        return el

    def get_publisher(self):
        el = ET.Element('publisher')
        el.text = 'Louisiana State University Special Collections'
        return el

    def get_addressline(self):
        el = ET.Element('addressline')
        el.text = 'Hill Memorial Library\nBaton Rouge, LA 70803-3300\nhttp://www.lib.lsu.edu/special'
        return el

    def get_date(self):
        el = ET.Element('date')
        el.text = self.extract_date()
        return el

    def extract_date(self):
        return self.element_tree.xpath('//page[@number="1"]/text[@width>"20"]')[-1].text.strip()

    def get_archdesc(self):
        default_stub = "Element not pulled from pdf"

        archdesc = ET.Element('archdesc', attrib={'level': default_stub, 'relatedencoding': 'MARC21', 'type': default_stub})  # duped info from ead level??

        a = ET.SubElement(archdesc, 'did')
        a1 = ET.SubElement(a, 'head')
        a1.text = 'Overview of the Collection'
        a2 = ET.SubElement(a, 'physdesc', attrib={'label': 'Quantity: ', 'encodinganalog': '300$a', })
        a2a = ET.SubElement(a2, 'extent',)
        a2a.text = default_stub
        a3 = ET.SubElement(a, 'unitdate', attrib={'label': 'Dates:', 'type': 'inclusive', 'encodinganalog': '245$f', 'type': default_stub, })
        a3.text = default_stub
        a4 = ET.SubElement(a, 'unitdate', attrib={'label': 'Dates:', 'type': 'bulk', 'encodinganalog': default_stub, 'type': default_stub, })
        a4.text = default_stub
        a5 = ET.SubElement(a, 'langmaterial')
        a5a = ET.SubElement(a5, 'language', attrib={'langcode': default_stub, })
        a5a.text = default_stub
        a6 = ET.SubElement(a, 'abstract', attrib={'label': "Abstract", 'encodinganalog': "520$a", })
        a6.text = default_stub
        a7 = ET.SubElement(a, 'repository', attrib={'label': 'Repository', 'encodinganalog': '825$a'})
        a7a = ET.SubElement(a7, 'corpname')
        a7a.text = default_stub
        a7b = ET.SubElement(a7, 'subarea')
        a7b.text = default_stub
        a8 = ET.SubElement(a, 'physloc')
        a8.text = default_stub
        a9 = ET.SubElement(a, 'origination', attrib={'label': 'Creator: '})
        a9a = ET.SubElement(a9, 'persname', attrib={'encodinganalog': "100"})
        a9a.text = default_stub
        a9b = ET.SubElement(a9, 'corpname', attrib={'encodinganalog': "110"})
        a9b.text = default_stub
        a10 = ET.SubElement(a, 'unitid', attrib={'countrycode': "US", 'encodinganalog': "099", 'label': "Identification: ", 'repositorycode': default_stub, })
        a10.text = default_stub
        a11 = ET.SubElement(a, 'unittitle', attrib={'encodinganalog': "245$a", 'label': "Title: "})
        a11.text = default_stub

        b = ET.SubElement(archdesc, 'accessrestrict')
        b1 = ET.SubElement(b, 'head')
        b1.text = "Access Restrictions"
        b2 = ET.SubElement(b, 'p')
        b2.text = default_stub
        # possibly b2.text will always be "There are no access restrictions on this material."

        c = ET.SubElement(archdesc, 'relatedmaterial', attrib={'encodinganalog': '544 1'})
        c1 = ET.SubElement(c, 'head')
        c1.text = "Related Collections"
        c2 = ET.SubElement(c, 'p')
        c2.text = default_stub

        d = ET.SubElement(archdesc, 'userestrict', attrib={'encodinganalog': '540'})
        d1 = ET.SubElement(d, 'head')
        d1.text = "Copyright"
        d2 = ET.SubElement(d, 'p')
        d2.text = default_stub  # Copyright terms pulled from text

        e = ET.SubElement(archdesc, 'prefercite', attrib={'encodinganalog': '524'})
        e1 = ET.SubElement(e, 'head')
        e1.text = "Preferred Citation"
        e2 = ET.SubElement(e, 'p')
        e2.text = default_stub

        f = ET.SubElement(archdesc, 'bioghist', attrib={'encodinganalog': '545'})
        f1 = ET.SubElement(f, 'head')
        f1.text = "BIOGRAPHICAL/HISTORICAL NOTE"
        f2 = ET.SubElement(f, 'p')
        try:
            f2.text = self.convert_text_after_header_to_string('biog')
        except:
            f2.text = default_stub

        g = ET.SubElement(archdesc, 'scopecontent', attrib={'encodinganalog': '520'})
        g1 = ET.SubElement(f, 'head')
        g1.text = "Scope and Contents of the Collection"
        g2 = ET.SubElement(g, 'p')
        try:
            g2.text = self.convert_text_after_header_to_string('scope')
        except:
            g2.text = default_stub

        h = ET.SubElement(archdesc, 'relatedmaterial')
        i = ET.SubElement(archdesc, 'separatedmaterial')
        i1 = ET.SubElement(i, 'head')
        i1.text = 'Separated Material'
        # for paragraph in Separated Material:
        #     ix = ET.SubElement(i, 'p')
        #     ix.text = text of paragraph

        i2 = ET.SubElement(i, 'p')
        i2.text = default_stub
        j = ET.SubElement(archdesc, 'otherfindaid')  # optional

        k = ET.SubElement(archdesc, 'controlaccess')
        k1 = ET.SubElement(k, 'head')
        k1.text = "Subject and Genre Headings"
        # for subject_term_item in Index_Terms:
        #    kx = ET.SubElement(k, {persname, corpname, etc as string, attrib={'encodinganalog': "610", 'source': default_stub}
        #     source as aat, lcsh, local, etc if possible, else default_stub
        #    kx.text = value of subject term as string

        l = ET.SubElement(archdesc, 'acqinfo')
        l1 = ET.SubElement(l, 'head')
        l1.text = 'Acquisition Information'
        l2 = ET.SubElement(l, 'p')
        l2.text = default_stub

        m = ET.SubElement(archdesc, 'appraisal')
        n = ET.SubElement(archdesc, 'accruals')

        o = ET.SubElement(archdesc, 'dsc')
        # for i in Series list:
        #     add a o1, o1a, o1b in the format below
        # o1 = ET.SubElement(o, 'co1', attrib={'level': 'series'})
        # o1a = ET.SubElement(o1, 'unitid')
        # o1a.text = Name of the Series
        # o1b = ET.SubElement(o1, 'p')
        # o1b.text = Text below that header

        p = ET.SubElement(archdesc, 'arrangement', attrib={'encodinganalog': '351$a'})
        p1 = ET.SubElement(p, 'head')
        p1.text = 'Related Material'
        # for paragraph in Scope and Content:
        #     px = ET.SubElement(p, 'p')
        #     px.text = text of paragraph
        p2 = ET.SubElement(p, 'p')
        try:
            p2.text = self.convert_text_after_header_to_string('series')
        except:
            p2.text = default_stub

        q = ET.SubElement(archdesc, 'appraisal', attrib={'encodinganalog': "583"})
        q1 = ET.SubElement(q, 'head')
        q1.text = 'Appraisal Information'
        q2 = ET.SubElement(q, 'p')
        q2.text = default_stub

        r = ET.SubElement(archdesc, 'accruals', attrib={'encodinganalog': "584"})
        r1 = ET.SubElement(r, 'head')
        r1.text = 'Accruals'
        r2 = ET.SubElement(r, 'p')
        r2.text = default_stub

        ''' Should include <origination>, <unitid>, and <unittitle>...<origination> may have to be added later since we do not include creator names on our summary pages but <unittitle> and <unitid> should come from the title page. <unittitle> is the collection title portion of <titleproper>. <unitid> is the Mss. number. EAD documents differentiate between the collection title and the title of the finding aid. This was difficult to convey in the tag document since our finding only have title for the collection, not the finding aid itself. '''
        return archdesc



    @staticmethod
    def which_subject_heading_type(text):
        term_dict_set = get_term_set_dict()
        for subject_heading, values_set in term_dict_set.iteritems():
            if text in values_set:
                return subject_heading
        else:
            return None

    ''' Extra useful tidbits (for development) '''
    def print_xml_to_file(self):
        file_name = os.path.splitext(os.path.basename(self.url))[0]
        path_file_name = 'cached_pdfs/{}.xml'.format(file_name)
        with open(path_file_name, 'w') as f:
            f.write(etree.tostring(self.element_tree, pretty_print=True))

    def print_ead_to_file(self, ead):
        if 'exported_eads' not in os.listdir(os.getcwd()):
            os.mkdir('{}/exported_eads'.format(os.getcwd()))
        file_name = os.path.splitext(os.path.basename(self.url))[0]
        path_file_name = 'exported_eads/{}.xml'.format(file_name)
        with open(path_file_name, 'w') as f:
            f.write(ET.tostring(ead, encoding="UTF-8", method="xml"))


    #
    # def getDefListItem(self, label):
    #     address  = "/pdf2xml/page[@number=1]/text[contains(text(),'Compiled by')]/following-sibling::text[1]/text()"
    #     nodes_list = self.element_tree.xpath(address)
    #     if len(nodes_list) > 0:
    #         return nodes_list[0].strip()
    #     return ''
    #


if __name__ == '__main__':
    logger = L('log', 'd')
    reader = ReadNSV('testList.nsv')
    for uid in reader.getLines():
        url = 'http://lib.lsu.edu/sites/default/files/sc/findaid/{}.pdf'.format(uid)
        print url
        A = FindingAidPDFtoEAD(url, logger)
        A.run_conversion()
