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
                 # "CITE AS"
                 ]
        self.list_of_proven_answers = {'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf': {
            terms[0]: 4,
            terms[1]: 4,
            terms[2]: 18,
            terms[3]: 18,
            terms[4]: 5,
            terms[5]: 6, },
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf': {
            terms[0]: 4,
            terms[1]: 6,
            terms[2]: 7,
            # Fails - uses non-standard header 'SERIES AND SUBSERIES
            # DESCRIPTONS'
            terms[3]: 8,
            terms[4]: 15,
            terms[5]: 18, },
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf': {
            terms[0]: 4,
            terms[1]: 5,
            terms[2]: 6,
            terms[3]: 7,
            terms[4]: 10,
            terms[5]: 11, },
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf': {
            terms[0]: 4,
            terms[1]: 5,
            terms[2]: 18,
            terms[3]: 18,
            terms[4]: 7,
            terms[5]: 8, },
        }
        current_pdfs_proven_answers = self.list_of_proven_answers[self.url]

        for term, page_num in current_pdfs_proven_answers.iteritems():
            self.assertEquals(self.findaid.getpagenum(term)[0], page_num, '\n\nFor url :{}\nTerm: {}\nExpected Page #: {}\nActual Page #: {}\n'.format(
                self.url, term, page_num, self.findaid.getpagenum(term)[0]))

    def testGetRColData(self):
        # size = self.findaid.getrcoldata('Size.')
        pass

    def testGetAllText(self):
        expected_answers = {
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf':
                [('BIOGRAPHICAL/HISTORICAL NOTE', 'SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', u"Jesse Homer Bankston was born Oct. 7, 1907 to Allie Magee and Leon V. Bankston of Washington Parish, La. He was educated in local schools and received his Ruth Paine (1918\u20131997), daughter of Walter R. Paine, Sr. Ruth was a member of the Bankston began his career in government in 1940 under Governor As a management consultant, he was charged with the reorganization of state government. In 1942, he became an organizational specialist in the Louisiana Civil Service Department. Under Governor assistant in the Department of Institutions and later as the director of that same Department. The Department, which was created 1940 and re-organized in 1942, supervised all mental, tuberculosis, and general hospitals, together with the State Penitentiary and two institutions for delinquent youths. When Governor Earl K. Long left office in 1952, Bankston left state government to open a healthcare consulting firm. With Governor Long\u2019s return to office in 1956, Bankston was appointed the director of the newly established Department of Hospitals. He held this position until the summer of 1959, when he was dismissed after a dispute over the governor\u2019s mental health. After his dismissal, Bankston returned to his consulting firm, and began to work with Democratic Party candidates and issues. He also joined the boards of the newly established Louisiana Public Broadcasting, and State Board of Elementary and Secondary Education. Elected in 1968, he served on State Board of Elementary and Secondary Education for 28 years. During his tenure, he served as secretary and chairman of the Board. Bankston was also the longest serving member of the Louisiana Democratic State Central Committee, having served for 51 years until his death in 2010. In 2002, he was inducted into the Louisiana Political Hall of Fame. In addition to his political pursuits, he also served as president of the Baton Rouge YMCA, Young Men's Business Club, Mental Health Association, and Tuberculosis Society."),
                 ('SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'INDEX TERMS', u'The collection, consisting of correspondence, political files, printed items and photographs, reflects Jesse H. Bankston\u2019s involvement in Louisiana state government and the Louisiana Democratic Party. Correspondence discusses political elections, candidates, and government health services. Political files pertain to activities of the Democratic Party, Louisiana politicians, and Louisiana Department of Institutions and State Hospital Board. Printed items contain ephemera and published material. Ephemera include programs, invitations, campaign buttons and bumper stickers, and items relating to the Mardi Gras celebration in Washington, D. C. Published material includes books, serials, newspaper clippings, and scrapbooks relating to Louisiana politics, campaigns and the National Democratic Convention of 1976. Photographs contain portraits, group photographs, and snapshots, with group photographs making up a large part of this series. Early photographs show several Bankston family members (ca. 1930s-ca. 1957). The remaining images show politicians and members of the Democratic Party at political events. The collection also includes a few miscellaneous personal papers.'),
                 ('LIST OF SERIES AND SUBSERIES', 'SERIES DESCRIPTIONS', 'INDEX TERMS', 'Series I. Correspondence, 1937-2006, undated. Series II. Political Files 1953-2007, undated. Subseries 1. General Files, 1953-2007, undated. Subseries 2. Earl K. Long File, ca. 1953-2003, undated. Subseries 3. Louisiana Hospital Files, 1941-1959. Series III. Printed Items, 1924-2010, undated. Subseries 1. Ephemera, ca. 1924-2007, undated. Subseries 2. Published Material, ca. 1936-2010, undated. Series IV. Photographs, ca. 1930s-2005, undated. Series V. Personal Papers, 1933-1952, undated.'),
                 ('SERIES DESCRIPTIONS', 'INDEX TERMS', 'CONTAINER LIST', u'Series I. Correspondence, 1937-2006, undated. Correspondence spans seven decades and reflects Jesse Bankston\u2019s role in the Louisiana Democratic Party and in state government. Topics include political elections, candidates, and government health services. In his letters, Bankston also seeks employment (1940) and comments on higher education boards (1985). Also present is a list of businesses who hired female employees in Franklinton and Bogalusa; the list includes the average weekly wages of those employees (Feb. 23, 1940). A group of letters written in 1940 relate to Bankston\u2019s job search, with one letter expressing his desire to find employment outside the sphere of politics (March 18, 1940). Correspondence with the Department of Political Science, University of North Carolina at Chapel Hill, discusses his proposed research topic on Louisiana state government (April-June 1945). In his letter of resignation to the Chairman of State Department of Institutions, Bankston points out the accomplishments of his four-year tenure (Sept. 2, 1952). Letters also discuss Gillis Long\u2019s candidacy in the gubernatorial election (1963, 1969- 1971). Charles A. Patout mentions Long\u2019s likely opponents in that race and he comments that voter turnout would be low for the youth vote and high for the African American vote (Dec. 29, 1969). implementation of the new Medicaid program, and he suggests a curtailment in Charity Hospital services (Dec. 30, 1968). Several letters express gratitude to Bankston for his political support. Correspondents include John McKeithen (Feb. 14, 1964), Edwin Edwards (June 14, 1974), Senator Russell Long (July 2, 1962), Hubert Humphrey (Sept. 28, 1964), and Bill Clinton (May 20, 1987). Bankston also promotes his own candidacy as a delegate to the upcoming constitutional convention (ca. 1970). Series II. Political Files 1953-2007, undated. Subseries 1. General Files, 1953-2007, undated. This subseries pertains to the activities of the Democratic State Central Committee of Louisiana and the Louisiana Democratic Party. It contains speeches, lists of Party members and contributors, and press releases. Speeches relate to healthcare (undated), the role of government, government policies, and political candidates. Press releases for the Democratic State Central Committee of Louisiana pertain to the Democratic Convention (Dec. 1981-March 1982). Also present is an autobiography of businessman and politician, Robert Angelle of St. Martin Parish (1896-1979). Other materials of note include transcriptions of two interviews conducted with Bankston by archivist, Lewis M. Morris (March 10, 1983) and university student, Jeremy Hammett (April 8, 2005). In both interviews, he discusses his involvement in Louisiana politics. Additionally, there is a 45-rpm recording of a Jimmy Subseries 2. Earl K. Long File, ca. 1953-2003, undated. This group, comprised of correspondence and official statements, relates to Governor Earl K. Long\u2019s confinement to a psychiatric hospital in the summer of 1959. They provide updates on the governor\u2019s progress and state of mind. In personal narratives, Bankston describes his relationship to Long, and he recounts the events surrounding the hospitalization (July 8, 1986, Jan. May 16, 2002, undated). In an undelivered speech, Senator Russell Long praises his uncle\u2019s political achievements, and he comments on Earl Long\u2019s confinement (undated). as that of Senator Russell Long (Sept. 2, 2006). Correspondence written during 2002- 2003 pertains to the life and political accomplishments of Earl K. Long. Subseries 3. Louisiana Hospital Files, 1941-1959. This subseries contains budget requests, financial reports, and a status report submitted by the Department of Institutions (1941-1944), and minutes and reports of the Louisiana State Hospital Board (Sept. 27, 1956-June 18, 1959). Papers of the Hospital Board detail programs and regulations proposed and implemented by the Board. Series III. Printed Items, 1924-2010, undated. Subseries 1. Ephemera, 1924-2007, undated. Most items in this subseries relate to political campaigns and events. This group contains programs, invitations, campaign buttons and bumper stickers, and items relating to the Mardi Gras celebration in Washington, D. C. Additionally, Huey P. Long\u2019s opposition to the oil industry is explained in an open letter to the public in the form of a handbill (ca. 1924). Invitations extended to Jesse Bankston include inauguration ceremonies of presidents Jimmy Carter (1977) and Bill Clinton (1993), and Governor Kathleen Blanco of Louisiana (Jan. 2004). Also found in this group are Christmas cards sent by Governor Earl K. Long (ca. 1950, ca. 1957), and President Carter and Vice-President Mondale (1977-ca. 1979). Programs for the Capitol Correspondents Association Gridiron Show parody political figures, including Jesse Bankston (1960). Subseries 2. Published Material, 1936-2010, undated.. Published material includes books, serials, and newspaper clippings. The book, booklet attempts made by Governor Jimmie Davis and the Louisiana Legislature to circumvent a federal desegregation order (1960). An issue of the administration of Governor Sam Houston Jones (Oct. /Nov. 1971). senator\u2019s political achievements, and an issue of the Newspapers clippings report on political campaigns, political events, and the Louisiana Democratic Party. Series IV. Photographs, ca. 1930s-2005, undated. This series contains portraits, group photographs, and snapshots, with group photographs making up a large part of this series. Among the earliest in the series are group photographs of Bankston family members (ca. 1930s-ca. 1957). The remaining images show politicians and members of the Democratic Party at political events. Photographs of Jesse Bankston include portraits and snapshots, and photographs taken by the press when he served as the Director of the State Hospital (1951), shortly after his dismissal in 1959, and when he served on the State Board of Education. This series also includes photographs of Bill and Hillary Clinton (1992), Jimmy Carter (1976), Edwin Edwards (ca. 1970s), and General Troy Middleton (ca. 1970-1975). Series V. Personal Papers, 1933-1952, undated. This small group is comprised of social invitations, dance cards, Jesse Bankston\u2019s LSU diploma (1936), his employment history, and an agreement for improving the drainage on his subdivision lot in Baton Rouge (1952).'),
                 ],
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf':
                [('BIOGRAPHICAL/HISTORICAL NOTE', 'SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', u'William Acy, Jr., born in 1822, was a plantation owner in Tangipahoa Parish, Louisiana. He also served as Justice of the Peace of Ascension Parish, La. from 1885-1891. His father, William Acy, Sr., of the "Acey" family, emigrated from Hull, England, to the United States in the early 19th century. He lived in Baltimore, Maryland, then moved to General Wade Hampton\'s Millwood Plantation in South Carolina, and finally to Gen. Hampton\'s Point Houmas Plantation in Louisiana. William Acy, Jr. owned land in Louisiana and Mississippi, which included Standley Plantation in Carroll County, Mississippi. He married Margaret E. Stansbury in 1847, and after her death, he married Mrs. Mary Elizabeth Marchbanks Stevens, a widow, in 1865. He had one son, C. C. Acy. Among William Acy\u2019s most prominent acquaintances was Francis T. Nicholls, who served as Governor of Louisiana and Chief Justice of the Louisiana State Supreme Court.'),
                 ('SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'INDEX TERMS', u"Correspondence, legal, and financial papers of William Acy, Jr., comprise this collection. Personal papers consist primarily of correspondence with relatives and friends in Maryland and England. They relate personal news and social activities, and provide some genealogical information. Among them is a letter from a cousin reporting on the poor living conditions in England and apathy of the people (Aug. 15, 1873). Business correspondence provides legal advice from Acy\u2019s attorneys and friends. Correspondence of Francis T. Nicholls pertains to Acy's properties (1888-1892). Letters from T. H. Somerville concern Standley Plantation, in Greenwood, Mississippi (1898-1901), and those of R. N. Sims concern a law suit before the Louisiana Supreme Court (1872). Letters from his son, C. C. Acy, describe conditions and management problems at Standley Plantation. There is also a letter from a patient confined to Jackson State Hospital complaining of conditions and inquiring about the length of his stay at the facility (April 15, 1907). He also questions whether he may have been committed for political reasons. Additionally, there are numerous letters regarding litigation over the settlement of the estate of William Acy, Sr., who died in 1882. Approximately $40,000 was owed to him at his death along with possible rights to property in Louisiana and Mississippi. There are numerous copies of court records kept by Acy, Jr., documenting the progression of a lawsuit filed against him by his nephew, William B. Lynam, who claimed a share in the estate of William Acy, Sr. Other documents include commissions signed by Louisiana Governors Hebert, Wickliffe and Moore confirming Acy, Jr.'s election as Justice of the Peace of Ascension Parish (1855-1861); a petition to the court submitted by James H. Muse against William Acy, Jr., for slander (Dec. 21, 1882); and a certificate awarded to Acy by the Amite City Lodge, No. 175 of the Louisiana Grand Lodge of Freemasons (March 4, 1871). Other legal papers consist of deeds and documents regarding property Acy acquired in Louisiana and Mississippi; papers pertaining to the estates of William Acy, Sr. and Margaret Stansbury Acy; and a sample ballot for the State and Tangipahoa Parish election of 1900. Canceled checks, tax receipts, bills, and invoices comprise the financial paper. Printed materials consist of maps of Baltimore, Maryland (1901) and London (undated); a legal brief submitted to the Louisiana Supreme Court in the case of (1882); advertising handbills, broadsides, pamphlets, catalogs, and books pertaining to railway travel (1897, 1901, 1907, 1908); hypnosis (1898); treatment of disease; sale of books, baby carriages, and farm equipment, including a cotton gin (1898). Among the medical printed materials is (1901) and prominent Southerners on the success of treatments. Additional printed volumes include the (April 1889, 1894, 1899, 1900). Photographs include cartes des visites, a cabinet card and a tintype, mostly of unidentified individuals. Photographs of family members include Elizabeth Stansbury Acy (1859), Mary Elizabeth Marchbanks Stevens Acy (1887), and William Acy, Sr. (1856). Bank books (1866- 1883, 1897-1902), memorandum books (1877-1903) and record books (1850-1899) comprise the manuscript volumes."),
                 ('LIST OF SERIES AND SUBSERIES', 'SERIES DESCRIPTIONS', 'INDEX TERMS', ''),
                 ('SERIES DESCRIPTIONS', 'INDEX TERMS', 'CONTAINER LIST', ''),
                 ],
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf':
                [('BIOGRAPHICAL/HISTORICAL NOTE', 'SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'Lewis Guion, the son of a sugar planter, was a jurist of Lafourche Parish, Louisiana. He studied law at the University of Virginia and practiced law in Thibodaux and New Orleans, Louisiana. On March 12, 1862, Guion enlisted as an officer in Company H of the 26th Louisiana Infantry Regiment under the leadership of Colonel Duncan S. Cage. After the Civil War, Guion established a sugar planting partnership with his brother-in- law, Francis T. Nicholls.'),
                 ('SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'INDEX TERMS', "The diary describes Guion's departure from New Orleans (Apr. 24, 1862), his Company's march from Camp Moore to Donaldsonville, Baton Rouge, and Greensburg (May 4, 1862), and military activities around Chickasaw Bayou and Yazoo Lake (Dec. 24-29, 1862). Entries after May 18, 1863 give a daily account of the Siege of Vicksburg and events following the siege. Entries describe routine activities, the receipt of Northern and Southern newspapers by the besieged, the arrival of couriers from Johnston's army, camp food, and daily rations. The diary lists names and gives total numbers of daily casualties during the siege, recording information about individuals killed."),
                 ('LIST OF SERIES AND SUBSERIES', 'SERIES DESCRIPTIONS', 'INDEX TERMS', ''),
                 ('SERIES DESCRIPTIONS', 'INDEX TERMS', 'CONTAINER LIST', ''),   
                 ],
            }
        
        current_pdfs_expected_answers = expected_answers[self.url]
        for our_tuple in current_pdfs_expected_answers:
            firstheader, secondheader, backupheader, return_value = our_tuple
            self.assertEquals(self.findaid.getalltext(firstheader, secondheader, backupheader), return_value, '\n\nFor url :{}\nHeaders: {}, {}, {}\nExpected return value: {}\nActual return value: {}\n'.format(
                self.url, firstheader, secondheader, backupheader, return_value, self.findaid.getalltext(firstheader, secondheader, backupheader)))


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(
        EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf'))
    suite.addTest(ParametrizedTestCase.parametrize(
        EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf'))
    suite.addTest(ParametrizedTestCase.parametrize(
        EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf'))
    suite.addTest(ParametrizedTestCase.parametrize(
        EadTest, url='http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf'))
    unittest.TextTestRunner(verbosity=2).run(suite)

# styles
# pre 2010 is really funky
# 2010 - 2013 standardization happened in 2010, some small change in style happened before 2013
# after 2013 is good
