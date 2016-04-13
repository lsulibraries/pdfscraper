#!/usr/bin/env python2.7

# python2 required due to scraperwiki not yet ported to python3

import os
import re
import urllib2
import logging

import scraperwiki
import lxml.etree as ET

from terms_dict_set import terms_dict_set
from langs_and_abbr import get_langs_and_abbr
from no_outline_pdfs import no_outline_pdfs_COI
from ParseTableofContents import ParseTableofContents as ParseTOC


def which_subject_heading_type(text):
    for (subject_heading, MARCencoding), source_dict in terms_dict_set.iteritems():
        for source, item_set in source_dict.iteritems():
            if text in item_set:
                return (subject_heading, MARCencoding, source)

def abbreviate_lang(language):
    lang_abbr_dict = get_langs_and_abbr()
    if language.lower() in lang_abbr_dict:
        return lang_abbr_dict[language.lower()]

def get_pdf_length(pdf_etree):
    list_of_all_page_nums = [int(i) for i in pdf_etree.xpath('//page/@number')]
    return max(list_of_all_page_nums)

def read_url_return_etree(url):
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    xmldata = bytes(bytearray(xmldata, encoding='utf-8'))
    element_tree = ET.fromstring(xmldata)
    return element_tree

def read_file_return_etree(uid):
    with open('cached_pdfs/{}.pdf'.format(uid), 'r') as f:
        pdfdata = f.read()                                    # str
    xmldata = scraperwiki.pdftoxml(pdfdata)                   # unicode
    xmldata = bytes(bytearray(xmldata, encoding='utf-8'))     # str
    element_tree = ET.fromstring(xmldata)
    return element_tree

def print_ead_to_file(uid, ead):
    if 'exported_eads' not in os.listdir(os.getcwd()):
        os.mkdir('{}/exported_eads'.format(os.getcwd()))
    path_file_name = 'exported_eads/{}.xml'.format(uid)
    with open(path_file_name, 'w') as f:
        f.write(ET.tostring(ead, encoding="utf-8", method="xml"))

def print_xml_to_file(uid, xml):
    if 'starting_xmls' not in os.listdir(os.getcwd()):
        os.mkdir('starting_xmls')
    path_file_name = 'starting_xmls/{}.xml'.format(uid)
    with open(path_file_name, 'w') as f:
        f.write(ET.tostring(xml, pretty_print=True))


class FindingAidPDFtoEAD():
    def __init__(self, url):
        self.uid = os.path.splitext(os.path.basename(url))[0]
        self.url = url
        logging.basicConfig(filename='log', level=logging.INFO)
        logging.info('{}'.format(self.uid))
        try:
            self.element_tree = read_file_return_etree(self.uid)
        except IOError:
            self.element_tree = read_url_return_etree(self.url)
        self.run_conversion()

    def run_conversion(self):
        # print ET.tostring(self.element_tree, pretty_print=True)             # dev only
        print_xml_to_file(self.uid, self.element_tree)
        if self.grab_contents_of_inventory():
            contents_of_inventory = self.grab_contents_of_inventory()
        else:
            contents_of_inventory = no_outline_pdfs_COI[self.uid]
        self.c_o_i_ordered = sorted(contents_of_inventory, key=lambda item: int(item[1][0]))
        self.summary_columns = self.get_columns_after_summary()
        compiled_ead = self.get_ead()
        print_ead_to_file(self.uid, compiled_ead)

    def grab_contents_of_inventory(self):
        if self.element_tree.xpath('//outline'):
            return [
                (elem.text.encode('ascii', 'ignore'), (int(elem.get('page')), int(elem.get('page'))))
                for elem in self.element_tree.xpath('//outline')[0].iter()
                if elem.tag == 'item'
                ]

    def get_columns_after_summary(self):
        summary_header_pages = [elem for elem in self.c_o_i_ordered if 'summ' in elem[0].lower()]
        if summary_header_pages:
            header, (beginning_page, end_page) = summary_header_pages[0]
            summary_page_elem = self.element_tree.xpath('//page[@number="{}"]'.format(beginning_page))[0]
            return ParseTOC.get_table(summary_page_elem)
        return None

    def convert_text_after_header_to_string(self, header_snippet):
        for pos, i in enumerate(self.c_o_i_ordered):
            if header_snippet.lower() in i[0].lower():
                if pos == len(self.c_o_i_ordered) - 1:
                    return ' '.join(self.get_text_after_header(i)).decode("utf8")
                else:
                    return ' '.join(self.get_text_after_header(i, self.c_o_i_ordered[pos + 1])).decode("utf8")
        return None

    def convert_text_after_header_to_list(self, header_snippet):
        for pos, i in enumerate(self.c_o_i_ordered):
            if header_snippet.lower() in i[0].lower():
                if pos == len(self.c_o_i_ordered) - 1:
                    return self.get_text_after_header(i)
                else:
                    return self.get_text_after_header(i, self.c_o_i_ordered[pos + 1])
        return None

    def convert_text_in_column_to_string(self, column_snippet):
        if self.summary_columns:
            for i in self.summary_columns:
                print(column_snippet, i)
                if column_snippet.lower() in i.lower():
                    return self.summary_columns[i].decode('utf-8')
        return None

    def get_text_after_header(self, inventory_item, following_inventory_item=None):
        header, (beginning_page, end_page) = inventory_item
        beginning_page, end_page = int(beginning_page), int(end_page)
        following_header = ''
        if following_inventory_item:
            following_header, (following_beginning_page, following_end_page) = following_inventory_item
        elem_of_header = self.element_tree.xpath(
            '//page[@number="{}"]/text/b[text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{}")]]'.format(
                beginning_page, header.lower().strip()
                )
            )
        text_after_header = []
        for i in self.get_first_page_siblings_and_children(elem_of_header):
            if i.lower().strip() == following_header.lower().strip():
                break
            text_after_header.append(i.strip())
        if following_inventory_item:
            following_header, (following_beginning_page, following_end_page) = following_inventory_item
            following_beginning_page, following_end_page = int(following_beginning_page), int(following_end_page)
            if following_beginning_page - beginning_page > 1:
                for page in xrange(beginning_page + 1, following_beginning_page):
                    text = self.get_middle_page_siblings_and_childrent(page)
                    for i in text:
                        text_after_header.append(i.strip())
            if self.get_last_page_siblings_and_children(following_header, following_beginning_page):
                for i in self.get_last_page_siblings_and_children(following_header, following_beginning_page):
                    text_after_header.append(i.strip())
        else:
            for i in self.do_get_last_pages_if_last_header(beginning_page):
                if isinstance(i, list):
                    for string in i:
                        text_after_header.append(string.strip())
                elif isinstance(i, str):
                    text_after_header.append(i.strip())
        return text_after_header

    def get_first_page_siblings_and_children(self, elem_of_header):
        list_of_sibling_children_text = []
        if len(elem_of_header) < 1:
            return list_of_sibling_children_text
        elems_following = elem_of_header[0].getparent().itersiblings()
        for sibling in elems_following:
            sibling_str = ET.tostring(sibling, encoding="utf-8", method='text', ).strip()
            if sibling_str and len(sibling_str) > 0:
                list_of_sibling_children_text.append(sibling_str)
        return list_of_sibling_children_text

    def get_middle_page_siblings_and_childrent(self, page):
        list_of_sibling_children_text = []
        elems_following = self.element_tree.xpath('//page[@number="{}"]/text'.format(page))
        for sibling in elems_following:
            sibling_str = ET.tostring(sibling, encoding="utf-8", method='text', ).strip()
            if sibling_str and len(sibling_str) > 0:
                list_of_sibling_children_text.append(sibling_str)
        return list_of_sibling_children_text

    def get_last_page_siblings_and_children(self, end_header, end_page):
        header_xpath = self.element_tree.xpath(
            '''//page[@number="{}"]/text/b[text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{}")]]'''.format(
                end_page, end_header.lower().strip()
                )
            )
        list_of_sibling_children_text = []
        if header_xpath:
            elems_preceding = header_xpath[0].getparent().itersiblings(preceding=True)
            for sibling in elems_preceding:
                sibling_str = ET.tostring(sibling, encoding="utf-8", method='text', ).strip()
                if sibling_str and len(sibling_str) > 0:
                    list_of_sibling_children_text.append(sibling_str)
        list_of_sibling_children_text = list_of_sibling_children_text.reverse()
        return list_of_sibling_children_text

    def do_get_last_pages_if_last_header(self, beginning_page):
        beginning_page = int(beginning_page)
        temp_text_list = []
        count = 0
        while (get_pdf_length(self.element_tree) - beginning_page) - count > 0:
            temp_text_list.append(self.get_middle_page_siblings_and_childrent(beginning_page + 1 + count))
            count += 1
        return temp_text_list

    def get_ead(self):
        ead = ET.Element('ead', attrib={'relatedencoding': "MARC21", 'type': "inventory", 'level': "collection", })
        ead.append(self.get_eadheader())
        ead.append(self.get_archdesc())
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
        temp_title = self.extract_title()
        el.text = u"A GUIDE TO THE {}".format(unicode(temp_title)).title()
        return el

    def extract_title(self):
        # titleproper - needs to account for multiple lines in some docs
        wholetitle = []
        title_elem = self.element_tree.xpath('//page[@number="1"]/text[@top>="200" and @width>"10"]/b')
        for el in title_elem:
            wholetitle.append(el.text.strip())
        return ' '.join(wholetitle)

    def get_num(self):
        el = ET.Element('num', attrib={'type': 'Manuscript'})
        el.text = self.extract_mss()
        return el

    def extract_mss(self):
        title_elem = self.element_tree.xpath('//page[@number="1"]/text[@top>="200" and @width>"10"]/b')
        # figuring out what the top value of the last line of the title is
        if title_elem:
            titlelineend = title_elem[-1].getparent().get('top')
            # num - assume it is between 12 and 25 units below the last line of title
            #    (a better way might have been to take next text node)
            numlinenumberA = str(int(titlelineend) + 12)  # 347
            numlinenumberB = str(int(titlelineend) + 25)  # 360
            xpath_address = '//page[@number="1"]/text[@top>=' + numlinenumberA + ' and @top<=' + numlinenumberB + ']'
            if self.element_tree.xpath(xpath_address):
                mss_elem = self.element_tree.xpath(xpath_address)[0]
                return mss_elem.text
        return None

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
        author_elem = self.element_tree.xpath('//page[@number="1"]/text[text()[normalize-space(.)="Compiled by"]]')
        if author_elem:
            pdfauthor = author_elem[0].getnext().text.strip()
        else:
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
        el = ET.Element('address')
        for line in ['Hill Memorial Library', 'Baton Rouge, LA 70803-3300', 'http://www.lib.lsu.edu/special']:
            sub = ET.Element('addressline')
            sub.text = line
            el.append(sub)
        return el

    def get_date(self):
        el = ET.Element('date')
        el.text = self.extract_date()
        return el

    def extract_date(self):
        date_elem = self.element_tree.xpath('//page[@number="1"]/text[@width>"20"]')[-1]
        if date_elem.text:
            return date_elem.text.strip()
        return None

    def get_archdesc(self):
        default_stub = "Element not pulled from pdf"

        archdesc = ET.Element(
            'archdesc', attrib={'level': "collection", 'relatedencoding': 'MARC21', 'type': "inventory"})

        a = ET.SubElement(archdesc, 'did')
        a1 = ET.SubElement(a, 'head')
        a1.text = 'Overview of the Collection'

        a2 = ET.SubElement(a, 'physdesc', attrib={'label': 'Size', 'encodinganalog': '300$a', })
        a2a = ET.SubElement(a2, 'extent',)
        a2a.text = self.convert_text_in_column_to_string('siz')

        a3 = ET.SubElement(a, 'unitdate', attrib={'label': 'Dates:', 'type': 'inclusive', 'encodinganalog': '245$f'})
        a3.text = self.convert_text_in_column_to_string('inclusive')

        a4 = ET.SubElement(a, 'unitdate', attrib={'label': 'Dates:', 'type': 'bulk', 'encodinganalog': default_stub})
        a4.text = self.convert_text_in_column_to_string('bulk')

        a5 = ET.SubElement(a, 'langmaterial')
        lang_list = self.convert_text_in_column_to_string('langua')
        if not lang_list:
            logging.info('no lang list found')
        else:
            for i in lang_list.split(','):
                i = i.strip().replace('.', '').replace(',', '')
                if i:
                    if abbreviate_lang(i):
                        elem = ET.Element('language', attrib={'langcode': abbreviate_lang(i), })
                        elem.text = i
                        a5.append(elem)
                    else:
                        logging.info('{} lang not found, possible key value mismatch'.format(i.encode('ascii', 'ignore')))
                else:
                    logging.info('no language column found in contents of inventory')

        a6 = ET.SubElement(a, 'abstract', attrib={'label': "Summary", 'encodinganalog': "520$a", })
        a6.text = self.convert_text_in_column_to_string('sum')

        a7 = ET.SubElement(a, 'repository', attrib={'label': 'Repository', 'encodinganalog': '825$a'})
        a7a = ET.SubElement(a7, 'corpname')
        a7a.text = "Louisiana State University Special Collections"
        a7b = ET.SubElement(a7, 'subarea')
        a7b.text = "Louisiana and Lower Mississippi Valley Collection"

        a8 = ET.SubElement(a, 'physloc')
        a8.text = self.convert_text_in_column_to_string('stack')

        a9 = ET.SubElement(a, 'origination', attrib={'label': 'Creator: '})
        a9a = ET.SubElement(a9, 'persname', attrib={'encodinganalog': "100"})
        a9a.text = default_stub
        originator = self.get_titleproper().text
        if originator[0:15].lower() == 'a guide to the ':
            originator = originator[15:]
        if originator[-6:] == 'PAPERS':
            originator = originator[:-7]
            a9a.text = originator
        if originator[-5:] == 'DIARY':
            originator = originator.split('DIARY')[0]
            a9a.text = originator

        a9b = ET.SubElement(a9, 'corpname', attrib={'encodinganalog': "110"})
        a9b.text = default_stub

        a10 = ET.SubElement(
            a, 'unitid', attrib={'countrycode': "US", 'encodinganalog': "099", 'label': "Identification: ", 'repositorycode': 'lu', })
        a10.text = self.extract_mss()

        a11 = ET.SubElement(a, 'unittitle', attrib={'encodinganalog': "245$a", 'label': "Title: "})
        a11.text = self.extract_title().title()

        b = ET.SubElement(archdesc, 'accessrestrict', attrib={'encodinganalog': '506'})
        b1 = ET.SubElement(b, 'head')
        b1.text = "Access Restrictions"
        b2 = ET.SubElement(b, 'p')
        b2.text = self.convert_text_in_column_to_string('restriction')

        c = ET.SubElement(archdesc, 'relatedmaterial', attrib={'encodinganalog': '544 1'})
        c1 = ET.SubElement(c, 'head')
        c1.text = "Related Collections"
        c2 = ET.SubElement(c, 'p')
        c2.text = self.convert_text_in_column_to_string('related')

        d = ET.SubElement(archdesc, 'userestrict', attrib={'encodinganalog': '540'})
        d1 = ET.SubElement(d, 'head')
        d1.text = "Copyright"
        d2 = ET.SubElement(d, 'p')
        d2.text = self.convert_text_in_column_to_string('copyright')

        e = ET.SubElement(archdesc, 'prefercite', attrib={'encodinganalog': '524'})
        e1 = ET.SubElement(e, 'head')
        e1.text = "Preferred Citation"
        e2 = ET.SubElement(e, 'p')
        e2.text = self.convert_text_in_column_to_string('citat')

        f = ET.SubElement(archdesc, 'bioghist', attrib={'encodinganalog': '545'})
        f1 = ET.SubElement(f, 'head')
        f1.text = "BIOGRAPHICAL/HISTORICAL NOTE".title()
        f2 = ET.SubElement(f, 'p')
        f2.text = self.convert_text_after_header_to_string('biog')

        g = ET.SubElement(archdesc, 'scopecontent', attrib={'encodinganalog': '520'})
        g1 = ET.SubElement(f, 'head')
        g1.text = "Scope and Contents of the Collection"
        g2 = ET.SubElement(g, 'p')
        g2.text = self.convert_text_after_header_to_string('scop')

        h = ET.SubElement(archdesc, 'relatedmaterial')
        i = ET.SubElement(archdesc, 'separatedmaterial')
        i1 = ET.SubElement(i, 'head')
        i1.text = 'Separated Material'
        # for paragraph in Separated Material:
        #     ix = ET.SubElement(i, 'p')
        #     ix.text = text of paragraph

        i2 = ET.SubElement(i, 'p')
        i2.text = default_stub
        j = ET.SubElement(archdesc, 'otherfindaid')

        k = ET.SubElement(archdesc, 'controlaccess')
        k1 = ET.SubElement(k, 'head')
        k1.text = "Index Terms"
        if self.convert_text_after_header_to_list('index'):
            for i in self.convert_text_after_header_to_list('index'):
                try:
                    (subject_heading, MARCencoding, source) = which_subject_heading_type(i)
                    elem = ET.Element(subject_heading, attrib={'source': source, 'encodinganalog': MARCencoding})
                    elem.text = i
                    k.append(elem)
                except Exception as e:
                    if len(i) > 4 and re.search('[a-zA-Z]', i):
                        elem = ET.Element('subject', attrib={'source': 'local', 'encodinganalog': '650'}, )
                        elem.text = unicode(i, encoding='utf-8')
                        k.append(elem)
                    else:
                        pass
                        # logging.info('{} doesnt seem like an acceptable source to this script'.format(i))

        l = ET.SubElement(archdesc, 'acqinfo')
        l1 = ET.SubElement(l, 'head')
        l1.text = 'Acquisition Information'
        l2 = ET.SubElement(l, 'p')
        l2.text = default_stub

        m = ET.SubElement(archdesc, 'appraisal')
        n = ET.SubElement(archdesc, 'accruals')

        o = ET.SubElement(archdesc, 'dsc', attrib={'type': 'in-depth'})
        o1 = ET.SubElement(o, 'head')
        o1 = ET.SubElement(o, 'c01', attrib={'level': 'series'})
        o2 = ET.SubElement(o1, 'did')
        o3 = ET.SubElement(o1, 'scopecontent')
        o4 = ET.SubElement(o3, 'p')
        o4.text = self.convert_text_after_header_to_string('series')
        o2a = ET.SubElement(o2, 'unitid')
        o2a.text = default_stub

        p = ET.SubElement(archdesc, 'arrangement', attrib={'encodinganalog': '351$a'})
        p1 = ET.SubElement(p, 'head')
        p1.text = 'Related Material'
        p2 = ET.SubElement(p1, 'p')
        p2.text = self.convert_text_in_column_to_string('related')

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

        return archdesc


if __name__ == '__main__':
    # single file
    # uid = '0005m'
    # url = 'http://lib.lsu.edu/sites/default/files/sc/findaid/{}.pdf'.format(uid)
    # FindingAidPDFtoEAD(url)

    # list of files
    filename = 'findaid_list.txt'
    with open(filename, 'r') as f:
        for uid in f.readlines():
            uid = uid.strip()
            url = 'http://lib.lsu.edu/sites/default/files/sc/findaid/{}.pdf'.format(uid)
            print(uid)
            FindingAidPDFtoEAD(url)
