#!/usr/bin/env python2.7

import unittest
from PdfScraperWikiPage import PdfScraperWikiPage as Page
from lxml import etree

class TestPageMethods(unittest.TestCase):

    def setUp(self):
        self.fixture = self.tree = etree.fromstring('''
            <page number="3" position="absolute" top="0" left="0" height="1188" width="918">
    <fontspec id="3" size="15" family="Times" color="#000000"/>
<text top="58" left="135" width="238" height="16" font="1"><b>JESSE BANKSTON PAPERS </b></text>
<text top="58" left="459" width="5" height="16" font="1"><b> </b></text>
<text top="58" left="748" width="80" height="16" font="1"><b>Mss. 5078 </b></text>
<text top="79" left="135" width="82" height="16" font="0">1924-2010 </text>
<text top="79" left="459" width="367" height="16" font="1"><b>SPECIAL COLLECTIONS, LSU LIBRARIES </b></text>
<text top="1117" left="414" width="95" height="16" font="0">Page 3 of 11 </text>
<text top="112" left="135" width="5" height="16" font="0"> </text>
<text top="133" left="135" width="100" height="16" font="1"><b>SUMMARY </b></text>
<text top="154" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="174" left="135" width="40" height="16" font="1"><b>Size. </b></text>
<text top="174" left="292" width="97" height="16" font="0">2.3 linear ft.  </text>
<text top="195" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="195" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="216" left="135" width="95" height="16" font="1"><b>Geographic </b></text>
<text top="236" left="135" width="77" height="16" font="1"><b>locations. </b></text>
<text top="215" left="292" width="215" height="16" font="0">Louisiana, Washington, D.C. </text>
<text top="257" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="257" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="278" left="135" width="123" height="16" font="1"><b>Inclusive dates. </b></text>
<text top="278" left="292" width="87" height="16" font="0">1924-2010. </text>
<text top="299" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="299" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="319" left="135" width="91" height="16" font="1"><b>Bulk dates. </b></text>
<text top="319" left="292" width="87" height="16" font="0">1956-1992. </text>
<text top="340" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="340" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="361" left="135" width="85" height="16" font="1"><b>Language. </b></text>
<text top="360" left="292" width="60" height="16" font="0">English </text>
<text top="381" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="381" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="402" left="135" width="85" height="16" font="1"><b>Summary. </b></text>
<text top="402" left="292" width="506" height="16" font="3">Correspondence, political files, newspaper clippings, campaign material, </text>
<text top="421" left="292" width="527" height="16" font="3">and photographs reflect Jesse H. Bankston’s involvement in Louisiana state </text>
<text top="441" left="292" width="339" height="16" font="3">government and the Louisiana Democratic Party.</text>
<text top="441" left="631" width="5" height="16" font="0"> </text>
<text top="461" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="461" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="482" left="135" width="120" height="16" font="1"><b>Restrictions on </b></text>
<text top="503" left="135" width="56" height="16" font="1"><b>access. </b></text>
<text top="482" left="292" width="518" height="16" font="0">Original letters of Hubert H. Humphrey (Sept. 28, 1964), Jimmy Carter </text>
<text top="503" left="292" width="460" height="16" font="0">(July 22, 1977), Bill Clinton (May 20, 1987) are restricted. Use </text>
<text top="523" left="292" width="96" height="16" font="0">photocopies. </text>
<text top="544" left="292" width="5" height="16" font="0"> </text>
<text top="565" left="135" width="63" height="16" font="1"><b>Related </b></text>
<text top="586" left="135" width="89" height="16" font="1"><b>collections. </b></text>
<text top="565" left="292" width="473" height="16" font="0">Jesse Bankston and Larry Bankston Oral History Interview, Mss. </text>
<text top="585" left="292" width="513" height="16" font="0">4700.1173.  Democratic State Central Committee of Louisiana Papers, </text>
<text top="606" left="292" width="510" height="16" font="0">Mss. 3760, Louisiana and Lower Mississippi Valley Collections, LSU </text>
<text top="627" left="292" width="502" height="16" font="0">Libraries, Baton Rouge, La. Louisiana and Lower Mississippi Valley </text>
<text top="647" left="292" width="335" height="16" font="0">Collections, LSU Libraries, Baton Rouge, La. </text>
<text top="668" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="668" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="689" left="135" width="88" height="16" font="1"><b>Copyright. </b></text>
<text top="689" left="292" width="502" height="16" font="0">For those materials not in the public domain, copyright is retained by </text>
<text top="710" left="292" width="519" height="16" font="0">the descendants of the creators in accordance with U.S. Copyright law.  </text>
<text top="731" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="731" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="751" left="135" width="72" height="16" font="1"><b>Citation. </b></text>
<text top="751" left="292" width="521" height="16" font="0">Jesse H. Bankston Papers, Mss. 5078, Louisiana and Lower Mississippi </text>
<text top="772" left="292" width="392" height="16" font="0">Valley Collections, LSU Libraries, Baton Rouge, La.  </text>
<text top="793" left="135" width="5" height="16" font="1"><b> </b></text>
<text top="793" left="292" width="5" height="16" font="1"><b> </b></text>
<text top="813" left="135" width="125" height="16" font="1"><b>Stack locations. </b></text>
<text top="813" left="292" width="195" height="16" font="0">116:24-25, OS:B, Vault:1  </text>
<text top="834" left="135" width="5" height="16" font="0"> </text>
<text top="854" left="135" width="5" height="16" font="0"> </text>
<text top="875" left="135" width="5" height="16" font="0"> </text>
<text top="896" left="135" width="5" height="16" font="0"> </text>
<text top="917" left="135" width="5" height="16" font="0"> </text>
<text top="937" left="135" width="5" height="16" font="0"> </text>
<text top="958" left="135" width="5" height="16" font="0"> </text>
<text top="958" left="351" width="5" height="16" font="0"> </text>
</page>

        ''')
        self.instance = Page(self.tree)


    def test_get_lines(self):
        lefts, tops = self.instance.get_lines()

    def test_get_columnar_lines(self):
        lines = self.instance.get_columnar_lines()
        # for top in lines:
            # print top

    def test_get_column_lefts(self):
        cols = self.instance.get_column_lefts()
        # print cols

    def test_get_col_cells(self):
        cols = self.instance.get_column_lefts()
        one, two = cols
        if one[0] > two[0]:
            left = two
            right = one
        else:
            left = one
            right = two

        left_cells = self.instance.get_col_cells(left[0])
        right_cells = self.instance.get_col_cells(right[0])

        table = {}
        i = 0
        for cell in left_cells:
            table[cell.strip()] = right_cells[i].strip()
            i += 1

    def test_get_table(self):
        table = Page.get_table(self.tree)
        for key,value in table.iteritems():
            print '{} ### {}'.format(key,value)



if __name__ == '__main__':
    unittest.main()