#!/usr/bin/env python2.7

import unittest
from PdfScraperWikiPage import PdfScraperWikiPage as Page
from lxml import etree

class TestPageMethods(unittest.TestCase):

    def setUp(self):
        self.fixture = self.tree = etree.fromstring('''
            <page number="3" position="absolute" top="0" left="0" height="1188" width="918">
                <text top="112" left="108" width="251" height="16" font="0"><b>ACY (WILLIAM) JR. PAPERS </b></text>
                <text top="106" left="360" width="5" height="24" font="1"> </text>
                <text top="106" left="459" width="5" height="24" font="1"> </text>
                <text top="112" left="707" width="108" height="16" font="0"><b>Mss. 717, 772 </b></text>
                <text top="127" left="108" width="82" height="24" font="1">1844-1909 </text>
                <text top="127" left="459" width="5" height="24" font="1"> </text>
                <text top="127" left="563" width="252" height="24" font="1">LSU Libraries Special Collections </text>
                <text top="1037" left="418" width="86" height="24" font="1">Page <b>3</b> of <b>9</b> </text>
                <text top="1058" left="108" width="5" height="24" font="1"> </text>
                <text top="190" left="459" width="5" height="16" font="0"><b> </b></text>
                <text top="211" left="108" width="96" height="16" font="0"><b>SUMMARY</b></text>
                <text top="205" left="204" width="5" height="24" font="1"> </text>
                <text top="225" left="108" width="5" height="24" font="1"> </text>
                <text top="246" left="108" width="5" height="24" font="1"> </text>
                <text top="273" left="116" width="35" height="16" font="0"><b>Size.</b></text>
                <text top="267" left="152" width="23" height="24" font="1">   </text>
                <text top="267" left="231" width="5" height="24" font="1"> </text>
                <text top="267" left="278" width="5" height="24" font="1"> </text>
                <text top="267" left="332" width="5" height="24" font="1"> </text>
                <text top="267" left="386" width="5" height="24" font="1"> </text>
                <text top="267" left="440" width="18" height="24" font="1">   </text>
                <text top="267" left="312" width="231" height="24" font="1">1 linear ft.; 18 mss. v.; 22 pr. v. </text>
                <text top="267" left="582" width="5" height="24" font="1"> </text>
                <text top="294" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="288" left="312" width="5" height="24" font="1"> </text>
                <text top="314" left="116" width="167" height="16" font="0"><b>Geographic locations.</b></text>
                <text top="309" left="283" width="5" height="24" font="1"> </text>
                <text top="308" left="312" width="251" height="24" font="1">Louisiana; Maryland; England.      </text>
                <text top="335" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="329" left="312" width="5" height="24" font="1"> </text>
                <text top="355" left="116" width="114" height="16" font="0"><b>Inclusive dates</b></text>
                <text top="350" left="230" width="9" height="24" font="1">. </text>
                <text top="350" left="278" width="5" height="24" font="1"> </text>
                <text top="350" left="312" width="87" height="24" font="1">1844-1909. </text>
                <text top="370" left="116" width="5" height="24" font="1"> </text>
                <text top="370" left="170" width="5" height="24" font="1"> </text>
                <text top="370" left="312" width="5" height="24" font="1"> </text>
                <text top="397" left="116" width="88" height="16" font="0"><b>Languages.</b></text>
                <text top="391" left="204" width="32" height="24" font="1">   </text>
                <text top="391" left="312" width="64" height="24" font="1">English. </text>
                <text top="418" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="412" left="312" width="5" height="24" font="1"> </text>
                <text top="439" left="116" width="80" height="16" font="0"><b>Summary.</b></text>
                <text top="433" left="197" width="5" height="24" font="1"> </text>
                <text top="433" left="231" width="9" height="24" font="1">  </text>
                <text top="432" left="312" width="478" height="24" font="1">Legal and financial papers, correspondence, memorandum books, </text>
                <text top="453" left="312" width="257" height="24" font="1">record books, and printed material. </text>
                <text top="480" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="474" left="312" width="5" height="24" font="1"> </text>
                <text top="501" left="116" width="111" height="16" font="0"><b>Organization. </b></text>
                <text top="495" left="312" width="315" height="24" font="1">Papers are arranged in chronological order. </text>
                <text top="521" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="515" left="312" width="5" height="24" font="1"> </text>
                <text top="542" left="116" width="171" height="16" font="0"><b>Restrictions on access.</b></text>
                <text top="536" left="288" width="5" height="24" font="1"> </text>
                <text top="536" left="332" width="5" height="24" font="1"> </text>
                <text top="536" left="312" width="116" height="24" font="1">No restrictions. </text>
                <text top="563" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="557" left="312" width="5" height="24" font="1"> </text>
                <text top="584" left="116" width="152" height="16" font="0"><b>Related collections. </b></text>
                <text top="577" left="312" width="35" height="24" font="1">N/A </text>
                <text top="604" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="598" left="312" width="5" height="24" font="1"> </text>
                <text top="625" left="116" width="84" height="16" font="0"><b>Copyright.</b></text>
                <text top="619" left="200" width="5" height="24" font="1"> </text>
                <text top="619" left="231" width="5" height="24" font="1"> </text>
                <text top="619" left="312" width="489" height="24" font="1">Physical rights are retained by the LSU Libraries.  Copyright of the </text>
                <text top="640" left="312" width="477" height="24" font="1">original materials is retained by descendants of the creators of the </text>
                <text top="660" left="312" width="356" height="24" font="1">materials in accordance with U.S. copyright law. </text>
                <text top="687" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="681" left="312" width="5" height="24" font="1"> </text>
                <text top="708" left="116" width="67" height="16" font="0"><b>Citation.</b></text>
                <text top="702" left="184" width="5" height="24" font="1"> </text>
                <text top="702" left="231" width="5" height="24" font="1"> </text>
                <text top="702" left="312" width="450" height="24" font="1">William Acy, Jr. Papers, Mss. 717, 722, Louisiana and Lower </text>
                <text top="722" left="312" width="445" height="24" font="1">Mississippi Valley Collections, LSU Libraries, Baton Rouge, </text>
                <text top="743" left="312" width="80" height="24" font="1">Louisiana.<b> </b></text>
                <text top="770" left="116" width="5" height="16" font="0"><b> </b></text>
                <text top="764" left="312" width="5" height="24" font="1"> </text>
                <text top="791" left="116" width="117" height="16" font="0"><b>Stack location. </b></text>
                <text top="785" left="234" width="9" height="24" font="1">  </text>
                <text top="784" left="312" width="117" height="24" font="1">E:1, F:1, OS:A. </text>
                <text top="805" left="108" width="5" height="24" font="1"> </text>
                <text top="805" left="324" width="5" height="24" font="1"> </text>
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
        table = self.instance.get_table()
        for key,value in table.iteritems():
            print '{} ### {}'.format(key,value)



if __name__ == '__main__':
    unittest.main()