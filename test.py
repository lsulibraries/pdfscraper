#! /usr/bin/env python2.7

import unittest
from pdfScraper import FindingAidPDFtoEAD
from lxml import etree
import lxml
import xml.etree.ElementTree as ET

# http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """

    def __init__(self, methodName='runTest', url=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.url = url

    @staticmethod
    def parametrize(testcase_klass, url=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, url=url))
        return suite


class EadTest(ParametrizedTestCase):

    def setUp(self):
        self.findaid = FindingAidPDFtoEAD(self.url)

    def test__init__(self):
        assert len(self.findaid.element_tree) > 0
        self.assertIsInstance(self.findaid.element_tree, lxml.etree._Element)

    def testget_first_page_siblings_and_children(self):
        fixture = '''<page>
            <text><b>Scope and Content Note</b></text>
            <text>The text of the note is here</text>
        </page>'''
        tree = etree.fromstring(fixture)
        header = tree.xpath('//text[contains(text(), "Scope")]')
        result = self.findaid.get_first_page_siblings_and_children(header)
        self.assertEquals(result, "The text of The note is here", "Failed to get expected text; result was {}".format(str(result)))

    def testWhich_Subject_Heading_Type(self):
        self.assertEquals(FindingAidPDFtoEAD.which_subject_heading_type('Amite City (La.)--History--20th century.'), 'geoname')
        self.assertEquals(FindingAidPDFtoEAD.which_subject_heading_type('goobergobber'), None)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(
       EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf'))
    suite.addTest(ParametrizedTestCase.parametrize(
        EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf'))
    suite.addTest(ParametrizedTestCase.parametrize(
       EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf'))
    unittest.TextTestRunner(verbosity=2).run(suite)
