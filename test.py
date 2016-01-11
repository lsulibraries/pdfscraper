#! python2.7

import unittest
from pdfScraper import FindingAidPDFtoEAD
import lxml

class EadTest(unittest.TestCase):

	def setUp(self):
		self.findaid = FindingAidPDFtoEAD('http://lib.lsu.edu/special/findaid/0826.pdf')

	def test__init__(self):
		assert len(self.findaid.root) > 0
		self.assertIsInstance(self.findaid.root, lxml.etree._Element)

	def testGetPageNum(self):
		terms = ["BIOGRAPHICAL/HISTORICAL NOTE", 
				"SCOPE AND CONTENT NOTE", 
				"LIST OF SERIES AND SUBSERIES", 
				"SERIES DESCRIPTIONS", 
				"INDEX TERMS", 
				"CONTAINER LIST"
				]
		list_of_proven_answers = 	{'http://lib.lsu.edu/special/findaid/0826.pdf': {
										terms[0]: 4, 
										terms[1]: 4,
										terms[2]: None,
										terms[3]: None,
										terms[4]: 5,
										terms[5]: 6,}
									}
		counter_outer, counter_inner = 0, 0
		for url, value in list_of_proven_answers.iteritems():
			for term, page_num in value.iteritems():
				self.assertEquals(self.findaid.getpagenum(term)[0], page_num, '\n\nFor url :{}\nTerm: {}\nExpected Page #: {}\nActual Page #: {}\n'.format(url, term, page_num, self.findaid.getpagenum(term)[0]))
				#print '\n\nFor url :{}\nTerm: {}\nObserved Page #: {}\nCalculated Page #: {}\n'.format(url, term, page_num, self.findaid.getpagenum(term)[0])


if __name__ == "__main__":
	unittest.main()


