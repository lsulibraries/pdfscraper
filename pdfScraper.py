#!/usr/bin/env python2.7

import scraperwiki
import urllib2
from lxml import etree
from lxml.builder import E
import re


class FindingAidPDFtoEAD():
    def __init__(self, url):
        self.url = url
        self.element_tree = self.read_url_return_etree(self.url)

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
        return self.element_tree

    def run_conversion(self):
        # print etree.tostring(self.element_tree, pretty_print=True)  # dev only
        # self.print_xml_to_file()                                    # dev only
        self.grab_contents_of_inventory()
        # headers_and_contents = dict()                               # get_text_after_header() not yet functional
        # for heading_and_pages in self.grab_contents_of_inventory():
        #     header, pages = heading_and_pages
        #     text_block = self.get_text_after_header(header, pages)
        #     headers_and_contents[header] = text_block

    '''               '''
    ''' new code flow '''
    def grab_contents_of_inventory(self):
        contents = self.element_tree.xpath('//page/text[b[contains(text(), "CONTENTS OF INVENTORY")]]/following-sibling::text/a')
        collapsed = self.collapse(contents)
        inventory = []
        for top, text in collapsed.iteritems():
            heading, page = re.findall('([A-Z\s\/a-z]+)[\s\.]+([0-9\-]+)', text)[0]
            pages_tuple = self.split_on_char('-', page)
            inventory.append((heading, pages_tuple))
        # print inventory
        return inventory

    def collapse(self, tree):
        collapsed = {}
        for elm in tree:
            top = elm.getparent().get('top')
            if top in collapsed:
                existing_text = collapsed[top] + ' ' + etree.tostring(elm, method='text').strip().lower()
            else:
                collapsed[top] = '' + etree.tostring(elm, method='text').strip().lower()
        return collapsed

    def split_on_char(self, char, text):
        if char in text:
            start, end = text.split(char)
        else:
            start, end = text, text
        return (start, end)

    def get_text_after_header(self, header, pages_tuple):
        # beginning_page, end_page = pages_tuple
        # ok, but fails to resume reading subtext at pagebreaks.
        # also fails on formatting changes
        # elem_of_header = self.element_tree.xpath('//page[@number="{}"]/text/b[text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{}")]]'.format(beginning_page, header.lower()))
        # elems_following = elem_of_header[0].getparent().itersiblings()
        # for sibling in elems_following:
        #     print sibling.text
        # unfinished.  It shall return all the text beneath a specified header.
        pass

    '''                    '''
    ''' original code flow '''
    def assemble_ead(self):

        # <langmaterial><!-- lang material may not be covered in finding aids -->
        #    <language encodinganalog="041" langcode="eng" scriptcode="latn">English in Latin script.</language>
        # </langmaterial>

        # todo add element deflist for things like : 'ENCODED BY', 'PROCESSED BY'

        # within the bioghist element, mark names (?): <persname>Mrs. Nellie M. Mingo</persname>

        pdfsubtitle = 'A Collection in the Louisiana and Lower Mississippi Valley Collections'
        pdfaddressline = 'Hill Memorial Library\nBaton Rouge, LA 70803-3300\nhttp://www.lib.lsu.edu/special'  # add phone numbers
        pdfpublisher = 'Louisiana State University Special Collections'
        pdfhead = 'SUMMARY'
        pdfcorpname = "Louisiana State University Special Collections"
        pdfsubarea = "Louisiana and Lower Mississippi Valley Collection"

        # titleproper - needs to account for multiple lines in some docs
        wholetitle = []
        titlelines = self.element_tree.xpath('//page[@number="1"]/text[@top>="200" and @width>"10"]/b')

        for el in titlelines:
            wholetitle.append(el.text.strip())
        pdftitleproper = 'A GUIDE TO THE ' + ' '.join(wholetitle)

        # figuring out what the top value of the last line of the title is
        titlelineend = titlelines[-1].getparent().get('top')

        # num - assume it is between 12 and 25 units below the last line of title
        #    (a better way might have been to take next text node)
        numlinenumberA = str(int(titlelineend) + 12)  # 347
        numlinenumberB = str(int(titlelineend) + 25)  # 360
        xpath_address = '//page[@number="1"]/text[@top>=' + numlinenumberA + ' and @top<=' + numlinenumberB + ']'
        mss_elem = self.element_tree.xpath(xpath_address)[0]
        mss_text = mss_elem.text
        if mss_text:
            pdfnum = mss_text.strip()
        else:
            # should we raise & catch exceptions here?
            print '\nAttention!!   MSS not digitally scanned from document: ', self.url, '\n'
            pdfnum = 'Attention!!   MSS not digitally scanned from document: {}'.format(self.url)

        # author - take next text node after the one that says "Compiled by" - with exception handling
        try:
            pdfauthor = self.element_tree.xpath('//page[@number="1"]/text[text()[normalize-space(.)="Compiled by"]]')[0].getnext().text.strip()
        except:
            pdfauthor = 'Special Collections Staff'

        # date - last node over "20" width on first page - "reformatted" or "revised" dates okay?
        pdfdate = self.element_tree.xpath('//page[@number="1"]/text[@width>"20"]')[-1].text.strip()

        # physdesc -

        # page 3 has a table - find the left of the two columns - can assume Size is the first and always there?
        elem_for_pos_of_left_column = self.element_tree.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="Size."]]')
        if elem_for_pos_of_left_column:
            xpos_of_left_column = elem_for_pos_of_left_column[0].getparent().get('left')
        # should we raise & catch Exceptions?
        else:
            # print '\nAttention!!  elem_for_pos_of_left_column not digitally scanned from document: {}\n'.format(self.url)
            xpos_of_left_column = '/nAttention!!  elem_for_pos_of_left_column not digitally scanned from document: {}'.format(self.url)

        # function finds right hand column data based on text of left hand column - just for page 3

        pdfextent = self.getrcoldata("Size.")
        pdfidates = self.getrcoldata("Inclusive dates.")
        pdfbdates = self.getrcoldata("Bulk dates.")

        pdflanguage = self.getrcoldata("Language.")
        if pdflanguage == "":
            pdflanguage = self.getrcoldata("Languages.")

        pdfabstract = self.getrcoldata("Summary.")

        pdfaccessrestrict = self.getrcoldata("Restrictions on access.")
        if pdfaccessrestrict == "":
            pdfaccessrestrict = self.getrcoldata("Access restrictions.")

        pdfrelatedmaterial = self.getrcoldata("Related collections.")
        if pdfrelatedmaterial == "":
            pdfrelatedmaterial = self.getrcoldata("Related collection.")

        pdfuserestrict = self.getrcoldata("Copyright.")
        pdfprefercite = self.getrcoldata("Citation.")

        pdfphysloc = self.getrcoldata("Stack locations.")
        if pdfphysloc == "":
            pdfphysloc = self.getrcoldata("Stack location.")

        # Then the getalltext function won't need a backupheader, and we can get all text by looping through available terms for appropriate sections
        pdfbioghist = self.getalltext("BIOGRAPHICAL/HISTORICAL NOTE", "SCOPE AND CONTENT NOTE", "LIST OF SERIES AND SUBSERIES")
        pdfscopecontent = self.getalltext("SCOPE AND CONTENT NOTE", "LIST OF SERIES AND SUBSERIES", "INDEX TERMS")
        almostListSeries = self.getalltext("LIST OF SERIES AND SUBSERIES", "SERIES DESCRIPTIONS", "INDEX TERMS")
        seriesdesc = self.getalltext("SERIES DESCRIPTIONS", "INDEX TERMS", "CONTAINER LIST")
        finalseries = self.seriesSplit(almostListSeries, "list", "head", "item", False)
        seriesdesc = self.seriesSplit(seriesdesc, "co1", "unitid", "p", True)

        # xmlcode = etree.XML(seriesSplit(seriesdesc,"co1","unitid","unitid"))
        # print etree.tostring(xmlcode, pretty_print=True)

        # using efactory

        ead = (
            E.ead(
                E.eadheader(
                    E.eadid('', countrycode='us', url=self.url),
                    E.filedesc(
                        E.titlestmt(
                            E.titleproper(pdftitleproper + '\n\t\t\t',
                                          E.num(pdfnum, type='Manuscript'),
                                          ),
                            E.subtitle(pdfsubtitle),
                            E.author(pdfauthor)
                        ),
                        E.publicationstmt(
                            E.publisher(pdfpublisher),
                            E.address(
                                E.addressline(pdfaddressline),
                            ),
                            E.date(pdfdate)
                        )
                    )
                ),
                E.archdesc(
                    E.did(
                        E.head(pdfhead),
                        E.physdesc('' + '\n\t\t', E.extent(pdfextent), label='Size', encodinganalog='300$a'),
                        E.unitdate(pdfidates, type='inclusive', label='Dates:', encodinganalog='245$f'),
                        E.unitdate(pdfbdates, type='bulk', label='Dates:'),
                        E.langmaterial(
                            E.language(pdflanguage, langcode='eng')
                        ),
                        E.abstract(pdfabstract, label='Summary'),
                        E.repository(
                            E.corpname(pdfcorpname),
                            E.subarea(pdfsubarea),
                            label='Repository:', encodinganalog='825$a'
                        ),
                        E.physloc(pdfphysloc),
                    ),
                    E.accessrestrict(
                        E.head("Restrictions on access"),
                        E.p(pdfaccessrestrict),
                    ),
                    E.relatedmaterial(
                        E.head("Related Collections"),
                        E.p(pdfrelatedmaterial),
                        encodinganalog='544 1'
                    ),
                    E.userestrict(
                        E.head("Copyright"),
                        E.p(pdfuserestrict),
                        encodinganalog='540'
                    ),
                    E.prefercite(
                        E.head("Preferred Citation"),
                        E.p(pdfprefercite),
                        encodinganalog='524'
                    ),
                    E.bioghist(
                        E.head("BIOGRAPHICAL/HISTORICAL NOTE"),
                        E.p(pdfbioghist),
                        encodinganalog='545'
                    ),
                    E.scopecontent(
                        E.head("SCOPE AND CONTENT NOTE"),
                        E.p(pdfscopecontent),
                        encodinganalog='520'
                    ),
                    # INDEX TERMS will need to be encoded all as 'subject' cuz we can't tell automatically...
                    # @source should usually be 'lcnaf'
                    # etree.XML(finalseries),   # commented out to silence errors
                    # etree.XML(seriesdesc)     # commented out to silence errors
                ),
                # E.acqinfo may need to be gleaned by humans, same for E.accruals
                # E.custodinfo, E.altformavail, E.appraisal
                # For required elements that must be inferred, insert placeholder text like:
                #   "Unknown - could not be automatically inferred"
                #
                # E.processinfo may need to be included
                level='collection', type='inventory', relatedencoding='MARC21'
            )
        )
        print etree.tostring(ead, pretty_print=True)
        # problem right now with ..... vs whitespace, getting some lists ['section pg'] others ['section', 'pg']

    def getrcoldata(self, lcolname):
        # this function may be obsolete, if we can expect "CONTENTS OF INVENTORY" to be correct.
        # maybe setup that test later..
        lcoldata = []
        # try it first as is, if not then try it again without the last character (usually a period)
        try:
            rcoltop = str(int(self.element_tree.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolname + '"]]')[0].getparent().get('top')))
            rcoltopbuffer = str(int(rcoltop)-10)
            afterrcoltop = str(int(self.element_tree.xpath('//page[@number="3"]/text[@left=' + xpos_of_left_column + ' and @top=' + rcoltop + ']/following::text[b]')[0].get('top'))-10)
            # check to see if it's last on page (it loops to top for some reason). if so hopefully one line is needed
            if afterrcoltop < rcoltop:
                afterrcoltop = str(int(rcoltop)+20)
            datalines = self.element_tree.xpath('//page[@number="3"]/text[@top>' + rcoltopbuffer + 'and @top<' + afterrcoltop + ' and @left>"200"]')
            for el in datalines:
                lcoldata.append(el.text.strip())
            pdfdata = ' '.join(lcoldata)
        except:
            try:
                lcolnameshort = lcolname[:-1]
                rcoltop = str(int(self.element_tree.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolnameshort + '"]]')[0].getparent().get('top')))
                rcoltopbuffer = str(int(rcoltop)-10)
                try:  # if it's the last in the column then hopefully its a single line
                    afterrcoltop = str(int(self.element_tree.xpath('//page[@number="3"]/text[@left=' + xpos_of_left_column + ' and @top=' + rcoltop + ']/following::text[b]')[0].get('top'))-10)
                except:
                    afterrcoltop = str(int(rcoltop)+15)
                datalines = self.element_tree.xpath('//page[@number="3"]/text[@top>' + rcoltopbuffer + 'and @top<' + afterrcoltop + ' and @left>"200"]')
                for el in datalines:
                    lcoldata.append(el.text.strip())
                pdfdata = ' '.join(lcoldata)
            except:
                try:  # split query - test each against different lines and expand the selection
                    lcolnamefirstpart = lcolname.rsplit(' ', 1)[0]
                    lcolnamelastword = lcolname.rsplit(' ', 1)[1]
                    rcoltop = str(int(self.element_tree.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolnamefirstpart + '"]]')[0].getparent().get('top')))
                    rcoltopbuffer = str(int(rcoltop)-10)
                    nextcoltop = str(int(self.element_tree.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolnamelastword + '"]]')[0].getparent().get('top')))
                    afterrcoltop = str(int(self.element_tree.xpath('//page[@number="3"]/text[@left=' + xpos_of_left_column + ' and @top=' + nextcoltop + ']/following::text[b]')[0].get('top'))-10)
                    datalines = self.element_tree.xpath('//page[@number="3"]/text[@top>' + rcoltopbuffer + 'and @top<' + afterrcoltop + ' and @left>"200"]')
                    for el in datalines:
                        lcoldata.append(el.text.strip())
                    pdfdata = ' '.join(lcoldata)
                except:
                    pdfdata = ' '
        # strip first character of data if it's a period or space
        try:
            if pdfdata[0] == "." or pdfdata[0] == " ":
                pdfdata = pdfdata[1:]
        except:
            pass
        # try:
        #     nextboldtext = self.element_tree.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolname + '"]]')[0].getparent().getnext().getchildren()[0].text
        # except:
        #     pass
        return pdfdata.strip()

    def getalltext(self, firstheader, secondheader, backupheader):
        firstpagenumber, firstheadertop = self.getpagenum(firstheader)
        secondpagenumber, secondheadertop = self.getpagenum(secondheader)
        backuppagenumber, backupheadertop = self.getpagenum(backupheader)

        if backuppagenumber < secondpagenumber or secondpagenumber == 19:
            secondpagenumber, secondheadertop = backuppagenumber, backupheadertop

        rawtext = []

        if secondheadertop:
            for p in range(firstpagenumber, secondpagenumber+1):
                if p == secondpagenumber:
                    bottom = secondheadertop
                else:
                    bottom = "1000"
                thingie = '//page[@number={}]/text[@top>={}and @top<{}]|//page[@number={}]/text[@top>={}and @top<{}]/b'.format(
                        str(p),
                        str(int(firstheadertop)+3),
                        str(int(bottom)-3),
                        str(p),
                        str(int(firstheadertop)+3),
                        str(int(bottom)-3)
                        )
                data = self.element_tree.xpath(thingie)
                for el in data:
                    if not el.text:  # removes blank nodes
                        continue
                    rawtext.append(el.text.strip())
        else:
            # should we throw & catch Exception?
            print '\nAttention!!   SecondHeaderTop == None.   The pdfscraper is broken in this case: ', self.url, '\n'

        textalmost = ' '.join(rawtext)
        alltext = ' '.join(textalmost.split())  # strips extra spaces
        return alltext

    def getpagenum(self, term):
        termtop = ""
        # @TODO return '', '' if term is not found
        for pagenumber in range(4, 19):
            try:
                termtop = str(int(self.element_tree.xpath('//page[@number='+str(pagenumber)+']/text/b[text()[normalize-space(.)="'+term+'"]]')[0].getparent().get('top')))
                break
            except:
                continue
        if pagenumber == 18:
            pagenumber, termtop = 18, None
        return pagenumber, termtop

    def seriesSplit(self, textinput, outerwrap, insidewrap, subwrap, check):
        outerwrapf = "<" + outerwrap + ">"
        outerwrapb = "</" + outerwrap + ">"
        insidewrapf = "<" + insidewrap + ">"
        insidewrapb = "</" + insidewrap + ">"
        subwrapf = "<" + subwrap + ">"
        subwrapb = "</" + subwrap + ">"

        d = "Series"
        s = [d + e for e in textinput.split(d) if e != ""]
        dd = "Subseries"
        serieses = []
        for a in s:
            l = [g for g in a.split(dd) if g != ""]
            serieses.append(l)
        finalseries = []
        for i, series in enumerate(serieses):
            finalseries.append(outerwrapf + insidewrapf + series[0] + insidewrapb)
            for ii, m in enumerate(series):
                if ii > 0:
                    finalseries.append(subwrapf + "Subseries" + series[ii] + subwrapb)
            finalseries.append(outerwrapb)
        finalseries.insert(0, "<arrangement encodinganalog='351'>")
        finalseries.append("</arrangement>")
        finalseries = "".join(finalseries)
        return finalseries


    ''' Extra useful tidbits (for development) '''

    # def print_xml_to_file(self):
    #     file_name = 'cached_pdfs/{}.xml'.format(self.url[-8:-4])
    #     with open(file_name, 'w') as f:
    #         f.write(etree.tostring(self.element_tree, pretty_print=True))
    #
    # def getDefListItem(self, label):
    #     address  = "/pdf2xml/page[@number=1]/text[contains(text(),'Compiled by')]/following-sibling::text[1]/text()"
    #     nodes_list = self.element_tree.xpath(address)
    #     if len(nodes_list) > 0:
    #         return nodes_list[0].strip()
    #     return ''
    #
    # def get_pdf_length(self):
    #     list_of_all_page_nums = [int(i) for i in self.element_tree.xpath('//page/@number')]
    #     return max(list_of_all_page_nums)


list_of_urls = [
                'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf',  # Bankston
                # 'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf',  # Acy papers
                'http://lib.lsu.edu/special/findaid/0826.pdf',  # Guion Diary
                'http://lib.lsu.edu/sites/default/files/sc/findaid/4745.pdf',  # mutltiline title #Problem with the Contents of Inventory
                # 'http://lib.lsu.edu/special/findaid/4452.pdf'  # Turnbull - multiple page biographical note
               ]

if __name__ == '__main__':
    for our_url in list_of_urls:
        print(our_url)
        A = FindingAidPDFtoEAD(our_url)
        A.assemble_ead()        # old code flow - transitioning away
        # A.run_conversion()    # new code flow - in development
