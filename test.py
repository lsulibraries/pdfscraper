#! /usr/bin/python2.7

import unittest
from pdfScraper import FindingAidPDFtoEAD
import lxml

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
		assert len(self.findaid.root) > 0
		self.assertIsInstance(self.findaid.root, lxml.etree._Element)

	def testGetPageNum(self):
		terms = ["BIOGRAPHICAL/HISTORICAL NOTE",
				"SCOPE AND CONTENT NOTE", 
				"LIST OF SERIES AND SUBSERIES", 
				"SERIES DESCRIPTIONS", 
				"INDEX TERMS", 
				"CONTAINER LIST",
				#"CITE AS"
				]
		self.list_of_proven_answers = 	{'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf': {
										terms[0]: 4, 
										terms[1]: 4,
										terms[2]: None,
										terms[3]: None,
										terms[4]: 5,
										terms[5]: 6,},
									'http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf': {
										terms[0]: 4,
										terms[1]: 6,
										terms[2]: 7,
										terms[3]: 8, # Fails - uses non-standard header 'SERIES AND SUBSERIES DESCRIPTONS'
										terms[4]: 15,
										terms[5]: 18,},
									'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf': {
										terms[0]: 4,
										terms[1]: 5,
										terms[2]: 6,
										terms[3]: 7,
										terms[4]: 10,
										terms[5]: 11,},
									'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf': {
										terms[0]: 4,
										terms[1]: 5,
										terms[2]: None,
										terms[3]: None,
										terms[4]: 7,
										terms[5]: 8,},
									}		
		allTerms = self.list_of_proven_answers[self.url]

		for term, page_num in allTerms.iteritems():
			self.assertEquals(self.findaid.getpagenum(term)[0], page_num, '\n\nFor url :{}\nTerm: {}\nExpected Page #: {}\nActual Page #: {}\n'.format(self.url, term, page_num, self.findaid.getpagenum(term)[0]))

	def testgetrcoldata(self):
		size = self.findaid.getrcoldata('Size.')
		self.assertEquals('hello', size)

if __name__ == "__main__":
	suite = unittest.TestSuite()
	suite.addTest(ParametrizedTestCase.parametrize(EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf'))
	suite.addTest(ParametrizedTestCase.parametrize(EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf'))
	suite.addTest(ParametrizedTestCase.parametrize(EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf'))
	suite.addTest(ParametrizedTestCase.parametrize(EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf'))
	unittest.TextTestRunner(verbosity=2).run(suite)

# styles
# pre 2010 is really funky
# 2010 - 2013 standardization happened in 2010, some small change in style happened before 2013
# after 2013 is good