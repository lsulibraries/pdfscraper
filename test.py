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

        #should we have a more unique dictionary of expected terms that are unique to the pdf
        #it seems like this would fix our problem with the 4452.pdf
        #or should we just make a new dictionary with the expected terms for each unique pdf?

    def testGetTextAfterHeader(self):
        sample_header_and_pages = {'http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf': (
            ('Biographical/Historical Note', (4, 4),
                """The Turnbull and Bowman families were cotton and sugar planters of West Feliciana Parish, Louisiana. John Turnbull and his brother, Walter, came to Louisiana from England in the 1770s. From their base in Louisiana, they traded furs, provisions, slaves, livestock, and agricultural produce including indigo and tobacco as partners in the firms Turnbull & Co., Turnbulls & Frazer, Turnbulls & Hood & Co., and Turnbull & Joyce. These companies traded goods in New Orleans, Natchez, Mobile, Pensacola, and London. They purchased pelts and skins from a number of Native Americans, probably of the Chickasaw and Choctaw tribes.  The Turnbulls were involved in the slave trade and may have brought slaves to Louisiana from Jamaica and the West Indies. Traders and merchants from Louisiana and England who were associated with the Turnbulls included John Joyce (d. 1798), John Reid, David Hodge, David Ross, Walter Hood, Alexander Frazer (d. ca. 1791), James Frazer, James Montgomery, James Fletcher, Eslava, and others. John Joyce was an Englishman who fought in Canada during the American Revolution on the side of the British. He traded furs, slaves, and goods in Mississippi, Louisiana, Florida, and Alabama. Joyce owned Magnolia Mound Plantation, in Baton Rouge, Louisiana, from 1791 until his death in 1798. Walter Turnbull resided in Nassau where he owned a cotton plantation and lived with his wife, Mary, his son, John, and at least two daughters.  By the 19th century, John Turnbull shifted his financial interests to planting and settled with his wife, Catherine (nee Rucker), and their children in Bayou Sara, West Feliciana Parish, Louisiana. Their children were John, Daniel (1796-1861), James F. (d. before 1831), Susannah (d. before 1831), Isabella (married Robert Semple), Sarah (married Lewis Stirling), and Walter (d. ca. 1838). Catherine managed many of her own business affairs; she jointly owned a plantation in St. Mary Parish with her son-in-law, John Towles, and had a house in New Orleans which she rented to Charles Norwood, a relative by marriage. She tutored children of planters and business people including Charles Norwood and Alexander Stirling.  Daniel Turnbull (1796-1861) became a successful planter, primarily owning cotton plantations.  In 1835, he founded Rosedown Plantation where he resided with his wife, Martha Hilliard Barrow Turnbull (1809-1896). Martha was raised on Highland Plantation in West Feliciana Parish. An avid horticulturist, she assembled a large collection of botanical specimens which she planted in extensive gardens at Rosedown. Children of this marriage included James Daniel (1836-1843), Daniel, William B. (1829-1856), and Sarah (1831-1914). In addition to Rosedown, Daniel operated Styopa, Catalpa, Middleplace, Hazelwood, Grove, Inheritance, Woodlawn, and De Soto plantations. Daniel Turnbull sold cotton through factors in New Orleans, including his nephew, A. M. Turnbull, who was member of the factorage A. M. Turnbull & Co.  In the 1820s, Daniel managed plantation property near St. Francisville jointly with his brother, James F. Turnbull, under the name D. & J. Turnbull. James died before 1831. Daniel' s son, William B. Turnbull, resided on De Soto Plantation in Bayou Sara. When he died (1856), William was survived by his wife, Caroline B. Turnbull (called "Caro"). Daniel Turnbull was the administrator of his estate.  The Bowman and Turnbull families were associated through the marriage of Daniel and Martha' s daughter, Sarah, to James P. Bowman (1832-1927). James was the son of Eliza Pirrie and her second husband, William R. Bowman (1800-1835), rector of Grace Episcopal Church in St. Francisville. Eliza Pirrie was the daughter of Lucretia (Lucy) Alston (1772-1833) and James Pirrie (1769-1824). James, Lucy' s second husband, served as alcalde under the Spanish governor Carlos de Grand-Pre. Eliza was raised at Oakley Plantation, which was founded by Ruffin Gray, the first husband of Lucy Alston. Ruffin Gray had moved to Louisiana from Virginia around 1770 when he received a Spanish land grant. In 1779, Ruffin was appointed alcalde in the Homochitto District by Manuel Gayoso de Lemos. Gray family members included Edmund (d. prior to 1777?), and Philip A., an attorney. Lucy and Ruffin had two children who survived to adulthood: Ruffin, Jr. (1796-1817), and Mary Anna Gray.  Eliza was the only child of Lucy and James Pirrie to reach adulthood. From her family, Eliza inherited Oakley, Home, Ogden, and Prospect plantations.  Eliza' s first marriage was to her cousin, Robert Hilliard Barrow (1795-1823), of Greenwood Plantation. With Robert, Eliza resided at Prospect Plantation and had one son, Robert Hilliard Barrow, Jr. The marriage of Eliza to her second husband, William R. Bowman, produced two children: Isabelle Bowman and James Pirrie Bowman (1832-1927). In 1840, Eliza married her last husband, Henry E. Lyons, a lawyer from Philadelphia. Their three children were Cora,Lucie, and Eliza. Lyons became a partner in a law practice with F. A. Boyle of West Feliciana Parish. In the 1850s, Henry Lyons traveled to California where he speculated in real estate and other financial ventures. He lived in San Francisco and became one of three men to serve on the first Supreme Court of California.  Sarah Turnbull inherited Rosedown and other plantations from her family. Like her mother, Sarah was a horticulturist. Her husband, James P. Bowman, produced cotton and sugar on Frogmoor and Bayou Grosse Tete plantations which he owned in Pointe Coupee Parish. In the 1890s, James was appointed to the Board of Administrators of the Insane Asylum of the State of Louisiana. He also served on the West Feliciana Parish School Board during the early 1900s. Upon her death in 1914, Sarah T. Bowman left her plantations and assets to her four daughters, Corrie (1872-1929), Isabel (1876-1951), Sarah (1869-1952), and Nina (1869-1955).  In 1956, after the death of the last Bowman sister, the Rosedown Plantation home and gardens were purchased and restored by Milton and Catherine Underwood."""
             ),
            ('Scope and Content Note', (6, 6),
                """Financial papers, correspondence, legal documents, personal papers, sheet music, printed items, and photographs covering the period 1771 to 1956 document lives of members of the Turnbull and Bowman families, cotton and sugar planters of West Feliciana Parish, Louisiana.  Some papers of the related Pirrie and Gray families are included. The largest series of the collection consists of financial papers which chiefly reflect activities of the Turnbull and Bowman families as planters in Louisiana from the early 1800s into the 20th century. These include early documents pertaining to John and Walter Turnbull and their business concerns as traders of furs, slaves, horses, indigo, and produce in Louisiana, Mississippi, and the West Florida region. Correspondence reflects subjects documented by the financial papers including the colonial fur trade, planting, and economic conditions in Louisiana. Some personal family letters relate to social events, religion, education, and domestic matters. Legal documents chiefly relate to the Bowman, Pirrie, and Gray families but include Turnbull family legal agreements and suits. Some documents relate to activities of Ruffin Gray and James Pirrie as alcaldes during the Spanish governance of Louisiana. Of special note in the plantation and personal papers are lists of slaves and lists of plants purchased. Music and other printed items were collected by members of the Turnbull, Bowman and related families. Photographs primarily depict members of the Bowman family and Rosedown Plantation. In addition to Rosedown Plantation, the papers document Oakley, Middleplace, Hazelwood, Homochitto, Grosse Tete, Catalpa, Styopa, Inheritance, De Soto, Grove, Frogmoor, Prospect, and Home plantations."""
             ),
        ),
        'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf': (
            ('Biographical/Historical Note', (4, 4), """Jesse Homer Bankston was born Oct. 7, 1907 to Allie Magee and Leon V. Bankston of Washington Parish, La. He was educated in local schools and received his Ruth Paine (1918&#8211;1997), daughter of Walter R. Paine, Sr. Ruth was a member of the Bankston began his career in government in 1940 under Governor As a management consultant, he was charged with the reorganization of state government. In 1942, he became an organizational specialist in the Louisiana Civil Service Department. Under Governor assistant in the Department of Institutions and later as the director of that same Department. The Department, which was created 1940 and re-organized in 1942, supervised all mental, tuberculosis, and general hospitals, together with the State Penitentiary and two institutions for delinquent youths. When Governor Earl K. Long left office in 1952, Bankston left state government to open a healthcare consulting firm. With Governor Long&#8217;s return to office in 1956, Bankston was appointed the director of the newly established Department of Hospitals. He held this position until the summer of 1959, when he was dismissed after a dispute over the governor&#8217;s mental health. After his dismissal, Bankston returned to his consulting firm, and began to work with Democratic Party candidates and issues. He also joined the boards of the newly established Louisiana Public Broadcasting, and State Board of Elementary and Secondary Education. Elected in 1968, he served on State Board of Elementary and Secondary Education for 28 years. During his tenure, he served as secretary and chairman of the Board. Bankston was also the longest serving member of the Louisiana Democratic State Central Committee, having served for 51 years until his death in 2010. In 2002, he was inducted into the Louisiana Political Hall of Fame. In addition to his political pursuits, he also served as president of the Baton Rouge YMCA, Young Men's Business Club, Mental Health Association, and Tuberculosis Society."""),
            ('Scope and Content Note', (5, 5), """The collection, consisting of correspondence, political files, printed items and photographs, reflects Jesse H. Bankston&#8217;s involvement in Louisiana state government and the Louisiana Democratic Party. Correspondence discusses political elections, candidates, and government health services. Political files pertain to activities of the Democratic Party, Louisiana politicians, and Louisiana Department of Institutions and State Hospital Board. Printed items contain ephemera and published material. Ephemera include programs, invitations, campaign buttons and bumper stickers, and items relating to the Mardi Gras celebration in Washington, D. C. Published material includes books, serials, newspaper clippings, and scrapbooks relating to Louisiana politics, campaigns and the National Democratic Convention of 1976. Photographs contain portraits, group photographs, and snapshots, with group photographs making up a large part of this series. Early photographs show several Bankston family members (ca. 1930s-ca. 1957). The remaining images show politicians and members of the Democratic Party at political events. The collection also includes a few miscellaneous personal papers."""),
        ),
        }
        if self.url not in sample_header_and_pages:
            self.assertEquals(False, True, "Missing expected values information for {}".format(self.url))
        current_pdfs_expected_answer = sample_header_and_pages[self.url]

        for section, page_nums, expected_text in current_pdfs_expected_answer:
            observed_result = self.findaid.get_text_after_header(
                (section, page_nums))
        # just tests first 20 characters of the texts
        self.assertEquals(observed_result[0][0:20], expected_text[0:20], 'For url: {}\nUnexpected Value for: {}\nGot: {}\nExpected: {}\n\n'.format(
            self.url, section, observed_result[0][0:10], expected_text[0:10]))




    def testget_first_page_siblings_and_children(self):
        fixture = '''<page>
            <text><b>Scope and Content Note</b></text>
            <text>The text of the note is here</text>
        </page>'''
        tree = etree.fromstring(fixture)
        header = tree.xpath('//text[contains(text(), "Scope")]')
        result = self.findaid.get_first_page_siblings_and_children(header)
        self.assertEquals(result, "The text of The note is here", "Failed to get expected text; result was {}".format(str(result)))

    def testGet_text_recursive(self):
        fixture = '''<page>
            <text>Scope <i>and</i> Content Note</text>
            <text>2 <i>line</i> eee.</text>
        </page>'''
        tree    = etree.fromstring(fixture)
        element = tree.xpath("//text[contains(text(), 'Scope')]")[0]
        result  = self.findaid.get_text_recursive(element)

        self.assertEquals(result, "Scope and Content Note")

    def test_getarchdesc(self):
        arch = self.findaid.get_archdesc()
        # print ET.tostring(arch)

    def test_get_ead(self):
        ead = self.findaid.get_ead()
        #print ET.tostring(ead)
        pass

    def test_get_index_terms(self):
        fixture   = self.findaid.read_url_return_etree(self.url)
        inventory = self.findaid.grab_contents_of_inventory()

        next = None
        has_index = False
        for head, pages in inventory:
            if has_index == True:
                next = head
                next_pages = pages
            if 'index' in head.lower():
                index_head = head
                index_pages = pages
                has_index  = True
        if has_index:
            result = self.findaid.get_text_after_header((index_head, index_pages), (next, next_pages))
            # print result
        else: 
            result = None

        for term in result:
            # print self.findaid.which_subject_heading_type(term)
        #print result
            pass

    def testWhich_Subject_Heading_Type(self):
        self.assertEquals(FindingAidPDFtoEAD.which_subject_heading_type('Amite City (La.)--History--20th century.'), 'geoname')
        self.assertEquals(FindingAidPDFtoEAD.which_subject_heading_type('goobergobber'), None)

if __name__ == "__main__":
    #  dev -- don't worry about tests calling out on the internet -- pdfScraper.read_url_return_etree() is switched to read from cached file.
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(
       EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf'))
    # suite.addTest(ParametrizedTestCase.parametrize(
    #    EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf'))
    suite.addTest(ParametrizedTestCase.parametrize(
        EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf'))
    suite.addTest(ParametrizedTestCase.parametrize(
       EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf'))
    unittest.TextTestRunner(verbosity=2).run(suite)

# styles
# pre 2010 is really funky
# 2010 - 2013 standardization happened in 2010, some small change in style happened before 2013
# after 2013 is good
