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


class PDFtoEAD():
    def __init__(self, url):
        self.uid = os.path.splitext(os.path.basename(url))[0]
        self.url = url
        logging.basicConfig(filename='log', level=logging.INFO)
        logging.info('{}'.format(self.uid))
        try:
            self.element_tree = read_file_return_etree(self.uid)
        except IOError:
            self.element_tree = read_url_return_etree(self.url)
        self.run_conversion(self.element_tree)

    def run_conversion(self, element_tree):
        # print ET.tostring(element_tree, pretty_print=True)             # dev only
        print_xml_to_file(self.uid, element_tree)
        if self.grab_contents_of_inventory(element_tree):
            contents_of_inventory = self.grab_contents_of_inventory(element_tree)
        else:
            contents_of_inventory = no_outline_pdfs_COI[self.uid]
        self.c_o_i_ordered = sorted(contents_of_inventory, key=lambda item: int(item[1][0]))
        self.summary_columns = self.get_summary(element_tree)
        compiled_ead = self.get_ead()
        self.alert_if_bad_summary(compiled_ead)
        print_ead_to_file(self.uid, compiled_ead)

    def grab_contents_of_inventory(self, element_tree):
        if element_tree.xpath('//outline'):
            return [
                (elem.text.encode('ascii', 'ignore'), (int(elem.get('page')), int(elem.get('page'))))
                for elem in element_tree.xpath('//outline')[0].iter()
                if elem.tag == 'item']

    def get_summary(self, element_tree):
        # no summary section
        if uid in ('3070', '4644'):
            return None
        # hardcoding page for finding summary, cause i'm lazy & worried introducing errors.
        if uid in ('0385', '0408', '1295', '1295sen', '1490company', '1490family', '1785', '3425',
                   '3637', '4171', '4625', '4777', '4966', 'folklife', ):
            pagenumber = '2'
        elif uid in ('4906'):
            pagenumber = '4'
        else:
            pagenumber = '3'
        elem_of_header = element_tree.xpath(
            '//page[@number="{}"]/text/b[text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{}")]]'.format(
                pagenumber, 'Summary'.lower().strip().replace('.', '')))
        text_list = self.convert_summary_into_text_list(elem_of_header)
        combined_bolds = self.combine_bolds(text_list)
        combined_normals = self.combine_normals(combined_bolds)
        summary_dict = self.dict_it(combined_normals)
        return summary_dict

    def convert_summary_into_text_list(self, elem_of_header):
        text_list = []
        for elem in elem_of_header[0].getparent().itersiblings():
            if elem.text and len(elem.text.strip()) > 0:
                text_list.append(['Text', elem.text.strip().strip('.').strip(',')])
            for bold_level in elem.getchildren():
                if bold_level.text and bold_level.text:
                    if len(bold_level.text.strip().strip('.').strip(',')) > 0:
                        text_list.append(['Bold', bold_level.text.strip().strip('.').strip(',')])
                    if bold_level.tail and len(bold_level.tail.strip().strip('.')):
                        text_list.append(['Tail', bold_level.tail.strip().strip('.').strip(',')])
        return text_list

    def combine_bolds(self, text_list):
        starts_with = ('size', 'geographic', 'inclusive', 'bulk', 'language', 'summary',
                       'organization', 'access', 'copyright', 'citation', 'stack', 'related', 'reproduction', 'arrangement'
                       )
        compressed_text_list = []
        for i in text_list:
            if i[0] == 'Bold':
                for starter in starts_with:
                    if starter in i[1].lower():
                        compressed_text_list.append(i)
                        break
                else:
                    for text_item in compressed_text_list[::-1]:
                        if text_item[0] == 'Bold':
                            text_item[1] = '{} {}'.format(text_item[1].encode('ascii', 'ignore'), i[1].encode('ascii', 'ignore')).encode('utf-8')
                            break
            elif i[0] in ('Text', 'Tail'):
                compressed_text_list.append(i)
        return compressed_text_list

    def combine_normals(self, compressed_text_list):
        final_text_list = []
        previous = 'Bold'
        for i in compressed_text_list:
            if i[0] == 'Bold':
                final_text_list.append(i)
                previous = 'Bold'
            else:
                if previous == 'Bold':
                    final_text_list.append(['Normal', i[1]])
                    previous = 'Normal'
                else:
                    final_text_list[-1][1] = '{} {}'.format(final_text_list[-1][1].encode('ascii', 'ignore'), i[1].encode('ascii', 'ignore')).encode('utf-8')
        return final_text_list

    def dict_it(self, final_text_list):
        summary_dict = dict()
        for count, i in enumerate(final_text_list):
            if count % 2 == 0 and len(final_text_list) > count + 1:
                summary_dict[i[1]] = final_text_list[count + 1][1]
        return summary_dict

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
                if column_snippet.lower() in i.lower():
                    return self.summary_columns[i].encode('utf-8', 'ignore')
        return None

    def get_text_after_header(self, inventory_item, following_inventory_item=None):
        header, (beginning_page, end_page) = inventory_item
        beginning_page, end_page = int(beginning_page), int(end_page)
        following_header = ''
        if following_inventory_item:
            following_header, (following_beginning_page, following_end_page) = following_inventory_item
        elem_of_header = self.element_tree.xpath(
            '//page[@number="{}"]/text/b[text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{}")]]'.format(
                beginning_page, header.lower().strip()))
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
        text = self.convert_text_in_column_to_string('siz')
        if text:
            try:
                a2a.text = text.replace('.', '')
            except:
                a2a.text = text.decode('utf-8').replace('.', '').encode('ascii', 'ignore')

        a3 = ET.SubElement(a, 'unitdate', attrib={'label': 'Dates:', 'type': 'inclusive', 'encodinganalog': '245$f'})
        text = self.convert_text_in_column_to_string('inclusive')
        if text:
            try:
                a3.text = text
            except:
                a3.text = text.decode('utf-8').encode('ascii', 'ignore')

        a4 = ET.SubElement(a, 'unitdate', attrib={'label': 'Dates:', 'type': 'bulk', 'encodinganalog': '245$g'})
        text = self.convert_text_in_column_to_string('bulk')
        if text:
            try:
                a4.text = text.replace('.', '')
            except:
                a4.text = text.decode('utf-8').replace('.', '').encode('ascii', 'ignore')

        a5 = ET.SubElement(a, 'langmaterial')
        lang_list = self.convert_text_in_column_to_string('langua')
        if not lang_list:
            logging.info('no lang list found')
        else:
            for lang in lang_list.split(','):
                lang = lang.strip().replace('.', '').replace(',', '')
                if lang:
                    lang_code = abbreviate_lang(lang)
                    if lang_code:
                        elem = ET.Element('language', attrib={'langcode': lang_code, })
                        elem.text = lang
                        a5.append(elem)
                    else:
                        logging.info('{} lang not found, possible key value mismatch'.format(lang.encode('ascii', 'ignore')))
                else:
                    logging.info('no language column found in contents of inventory')

        a6 = ET.SubElement(a, 'abstract', attrib={'label': "Summary", 'encodinganalog': "520$a", })
        text = self.convert_text_in_column_to_string('sum')
        if text:
            try:
                a6.text = text
            except:
                a6.text = text.decode('utf-8').encode('ascii', 'ignore')

        a7 = ET.SubElement(a, 'repository', attrib={'label': 'Repository', 'encodinganalog': '825$a'})
        a7a = ET.SubElement(a7, 'corpname')
        a7a.text = "Louisiana State University Special Collections"
        a7b = ET.SubElement(a7, 'subarea')
        a7b.text = "Louisiana and Lower Mississippi Valley Collection"

        a8 = ET.SubElement(a, 'physloc')
        text = self.convert_text_in_column_to_string('stack')
        if text:
            try:
                a8.text = text
            except:
                a8.text = text.decode('utf-8').encode('ascii', 'ignore')

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
        text = self.convert_text_in_column_to_string('restriction')
        if text:
            try:
                b2.text = text
            except:
                b2.text = text.decode('utf-8').encode('ascii', 'ignore')

        c = ET.SubElement(archdesc, 'relatedmaterial', attrib={'encodinganalog': '544 1'})
        c1 = ET.SubElement(c, 'head')
        c1.text = "Related Collections"
        c2 = ET.SubElement(c, 'p')
        text = self.convert_text_in_column_to_string('related')
        if text:
            try:
                c2.text = text
            except:
                c2.text = text.decode('utf-8').encode('ascii', 'ignore')

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
        text = self.convert_text_in_column_to_string('related')
        if text:
            try:
                p2.text = text
            except:
                p2.text = text.decode('utf-8').encode('ascii', 'ignore')

        q = ET.SubElement(archdesc, 'appraisal', attrib={'encodinganalog': "583"})
        q1 = ET.SubElement(q, 'head')
        q1.text = 'Appraisal Information'

        r = ET.SubElement(archdesc, 'accruals', attrib={'encodinganalog': "584"})
        r1 = ET.SubElement(r, 'head')
        r1.text = 'Accruals'

        return archdesc

    """bookkeeping & verification"""

    def alert_if_bad_summary(self, compiled_ead):
        summary_elems = dict()
        summary_elems['Size'] = compiled_ead.xpath('//physdesc/extent')[0]
        # Geographic Location is not searched for.
        summary_elems['Dates Inclusive'] = compiled_ead.xpath('//unitdate[@type="inclusive"]')[0]
        summary_elems['Dates Bulk'] = compiled_ead.xpath('//unitdate[@type="bulk"]')[0]
        if compiled_ead.xpath('//langmaterial/language'):
            summary_elems['Language'] = compiled_ead.xpath('//langmaterial/language')[0]
        summary_elems['Summary'] = compiled_ead.xpath('//abstract[@label="Summary"]')[0]
        # Organization is not searched for.
        if compiled_ead.xpath('//origination[@label="Creator"]/persname'):
            summary_elems['Creator persname'] = compiled_ead.xpath('//origination[@label="Creator"]/persname')[0]
        if compiled_ead.xpath('//origination[@label="Creator"]/corpname'):
            summary_elems['Creator corpname'] = compiled_ead.xpath('//origination[@label="Creator"]/corpname')[0]
        if compiled_ead.xpath('//unitid[@label="Identification"]'):
            summary_elems['MSS'] = compiled_ead.xpath('//unitid[@label="Identification"]')[0]
        if compiled_ead.xpath('//unittitle[@label="Title:"]'):
            summary_elems['Title'] = compiled_ead.xpath('//unittitle[@label="Title:"]')[0]
        summary_elems['Access Restrictions'] = compiled_ead.xpath('//accessrestrict/p')[0]
        summary_elems['Related Material'] = compiled_ead.xpath('//relatedmaterial/p')[0]
        summary_elems['Copyright'] = compiled_ead.xpath('//userestrict/p')[0]
        summary_elems['Citation'] = compiled_ead.xpath('//prefercite/p')[0]
        
        for name, element in summary_elems.items():
            if element.text is None:
                logging.info('no {}'.format(name))

if __name__ == '__main__':
    '''single file'''
    # uid = '2713'
    # url = 'http://lib.lsu.edu/sites/default/files/sc/findaid/{}.pdf'.format(uid)
    # print(uid)
    # PDFtoEAD(url)

    '''list of files'''
    filename = 'findaid_list.txt'
    with open(filename, 'r') as f:
        for uid in f.readlines():
            uid = uid.strip()
            url = 'http://lib.lsu.edu/sites/default/files/sc/findaid/{}.pdf'.format(uid)
            print(uid)
            PDFtoEAD(url)
