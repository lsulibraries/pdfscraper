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
    # def testGetPageNum(self):
    #     terms = ["BIOGRAPHICAL/HISTORICAL NOTE",
    #              "SCOPE AND CONTENT NOTE",
    #              "LIST OF SERIES AND SUBSERIES",
    #              "SERIES DESCRIPTIONS",
    #              "INDEX TERMS",
    #              "CONTAINER LIST",
    #              # "CITE AS"
    #              ]
    #     self.list_of_proven_answers = {'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf': {
    #         terms[0]: 4,
    #         terms[1]: 4,
    #         terms[2]: 18,
    #         terms[3]: 18,
    #         terms[4]: 5,
    #         terms[5]: 6, },
    #         'http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf': {
    #         terms[0]: 4,
    #         terms[1]: 6,
    #         terms[2]: 7,
    #         # Fails - uses non-standard header 'SERIES AND SUBSERIES 
    #         # DESCRIPTONS'
    #         terms[3]: 8,
    #         terms[4]: 15,
    #         terms[5]: 18, },
    #         'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf': {
    #         terms[0]: 4,
    #         terms[1]: 5,
    #         terms[2]: 6,
    #         terms[3]: 7,
    #         terms[4]: 10,
    #         terms[5]: 11, },
    #         'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf': {
    #         terms[0]: 4,
    #         terms[1]: 5,
    #         terms[2]: 18,
    #         terms[3]: 18,
    #         terms[4]: 7,
    #         terms[5]: 8, },
    #     }

    #     current_pdfs_proven_answers = self.list_of_proven_answers[self.url]
    #     for term, page_num in current_pdfs_proven_answers.iteritems():
    #         self.assertEquals(self.findaid.getpagenum(term)[0], page_num, '\n\nFor url :{}\nTerm: {}\nExpected Page #: {}\nActual Page #: {}\n'.format(
    #             self.url, term, page_num, self.findaid.getpagenum(term)[0]))


    def testGetRColData(self):
        # size = self.findaid.getrcoldata('Size.')
        pass

    def testGetAllText(self):
        expected_answers = {
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf':
                [('BIOGRAPHICAL/HISTORICAL NOTE', 'SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', u"Jesse Homer Bankston was born Oct. 7, 1907 to Allie Magee and Leon V. Bankston of Washington Parish, La. He was educated in local schools and received his Ruth Paine (1918\u20131997), daughter of Walter R. Paine, Sr. Ruth was a member of the Bankston began his career in government in 1940 under Governor As a management consultant, he was charged with the reorganization of state government. In 1942, he became an organizational specialist in the Louisiana Civil Service Department. Under Governor assistant in the Department of Institutions and later as the director of that same Department. The Department, which was created 1940 and re-organized in 1942, supervised all mental, tuberculosis, and general hospitals, together with the State Penitentiary and two institutions for delinquent youths. When Governor Earl K. Long left office in 1952, Bankston left state government to open a healthcare consulting firm. With Governor Long\u2019s return to office in 1956, Bankston was appointed the director of the newly established Department of Hospitals. He held this position until the summer of 1959, when he was dismissed after a dispute over the governor\u2019s mental health. After his dismissal, Bankston returned to his consulting firm, and began to work with Democratic Party candidates and issues. He also joined the boards of the newly established Louisiana Public Broadcasting, and State Board of Elementary and Secondary Education. Elected in 1968, he served on State Board of Elementary and Secondary Education for 28 years. During his tenure, he served as secretary and chairman of the Board. Bankston was also the longest serving member of the Louisiana Democratic State Central Committee, having served for 51 years until his death in 2010. In 2002, he was inducted into the Louisiana Political Hall of Fame. In addition to his political pursuits, he also served as president of the Baton Rouge YMCA, Young Men's Business Club, Mental Health Association, and Tuberculosis Society."),
                 ('SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'INDEX TERMS',
                  u'The collection, consisting of correspondence, political files, printed items and photographs, reflects Jesse H. Bankston\u2019s involvement in Louisiana state government and the Louisiana Democratic Party. Correspondence discusses political elections, candidates, and government health services. Political files pertain to activities of the Democratic Party, Louisiana politicians, and Louisiana Department of Institutions and State Hospital Board. Printed items contain ephemera and published material. Ephemera include programs, invitations, campaign buttons and bumper stickers, and items relating to the Mardi Gras celebration in Washington, D. C. Published material includes books, serials, newspaper clippings, and scrapbooks relating to Louisiana politics, campaigns and the National Democratic Convention of 1976. Photographs contain portraits, group photographs, and snapshots, with group photographs making up a large part of this series. Early photographs show several Bankston family members (ca. 1930s-ca. 1957). The remaining images show politicians and members of the Democratic Party at political events. The collection also includes a few miscellaneous personal papers.'),
                 ('LIST OF SERIES AND SUBSERIES', 'SERIES DESCRIPTIONS', 'INDEX TERMS',
                  'Series I. Correspondence, 1937-2006, undated. Series II. Political Files 1953-2007, undated. Subseries 1. General Files, 1953-2007, undated. Subseries 2. Earl K. Long File, ca. 1953-2003, undated. Subseries 3. Louisiana Hospital Files, 1941-1959. Series III. Printed Items, 1924-2010, undated. Subseries 1. Ephemera, ca. 1924-2007, undated. Subseries 2. Published Material, ca. 1936-2010, undated. Series IV. Photographs, ca. 1930s-2005, undated. Series V. Personal Papers, 1933-1952, undated.'),
                 ('SERIES DESCRIPTIONS', 'INDEX TERMS', 'CONTAINER LIST',
                  u'Series I. Correspondence, 1937-2006, undated. Correspondence spans seven decades and reflects Jesse Bankston\u2019s role in the Louisiana Democratic Party and in state government. Topics include political elections, candidates, and government health services. In his letters, Bankston also seeks employment (1940) and comments on higher education boards (1985). Also present is a list of businesses who hired female employees in Franklinton and Bogalusa; the list includes the average weekly wages of those employees (Feb. 23, 1940). A group of letters written in 1940 relate to Bankston\u2019s job search, with one letter expressing his desire to find employment outside the sphere of politics (March 18, 1940). Correspondence with the Department of Political Science, University of North Carolina at Chapel Hill, discusses his proposed research topic on Louisiana state government (April-June 1945). In his letter of resignation to the Chairman of State Department of Institutions, Bankston points out the accomplishments of his four-year tenure (Sept. 2, 1952). Letters also discuss Gillis Long\u2019s candidacy in the gubernatorial election (1963, 1969- 1971). Charles A. Patout mentions Long\u2019s likely opponents in that race and he comments that voter turnout would be low for the youth vote and high for the African American vote (Dec. 29, 1969). implementation of the new Medicaid program, and he suggests a curtailment in Charity Hospital services (Dec. 30, 1968). Several letters express gratitude to Bankston for his political support. Correspondents include John McKeithen (Feb. 14, 1964), Edwin Edwards (June 14, 1974), Senator Russell Long (July 2, 1962), Hubert Humphrey (Sept. 28, 1964), and Bill Clinton (May 20, 1987). Bankston also promotes his own candidacy as a delegate to the upcoming constitutional convention (ca. 1970). Series II. Political Files 1953-2007, undated. Subseries 1. General Files, 1953-2007, undated. This subseries pertains to the activities of the Democratic State Central Committee of Louisiana and the Louisiana Democratic Party. It contains speeches, lists of Party members and contributors, and press releases. Speeches relate to healthcare (undated), the role of government, government policies, and political candidates. Press releases for the Democratic State Central Committee of Louisiana pertain to the Democratic Convention (Dec. 1981-March 1982). Also present is an autobiography of businessman and politician, Robert Angelle of St. Martin Parish (1896-1979). Other materials of note include transcriptions of two interviews conducted with Bankston by archivist, Lewis M. Morris (March 10, 1983) and university student, Jeremy Hammett (April 8, 2005). In both interviews, he discusses his involvement in Louisiana politics. Additionally, there is a 45-rpm recording of a Jimmy Subseries 2. Earl K. Long File, ca. 1953-2003, undated. This group, comprised of correspondence and official statements, relates to Governor Earl K. Long\u2019s confinement to a psychiatric hospital in the summer of 1959. They provide updates on the governor\u2019s progress and state of mind. In personal narratives, Bankston describes his relationship to Long, and he recounts the events surrounding the hospitalization (July 8, 1986, Jan. May 16, 2002, undated). In an undelivered speech, Senator Russell Long praises his uncle\u2019s political achievements, and he comments on Earl Long\u2019s confinement (undated). as that of Senator Russell Long (Sept. 2, 2006). Correspondence written during 2002- 2003 pertains to the life and political accomplishments of Earl K. Long. Subseries 3. Louisiana Hospital Files, 1941-1959. This subseries contains budget requests, financial reports, and a status report submitted by the Department of Institutions (1941-1944), and minutes and reports of the Louisiana State Hospital Board (Sept. 27, 1956-June 18, 1959). Papers of the Hospital Board detail programs and regulations proposed and implemented by the Board. Series III. Printed Items, 1924-2010, undated. Subseries 1. Ephemera, 1924-2007, undated. Most items in this subseries relate to political campaigns and events. This group contains programs, invitations, campaign buttons and bumper stickers, and items relating to the Mardi Gras celebration in Washington, D. C. Additionally, Huey P. Long\u2019s opposition to the oil industry is explained in an open letter to the public in the form of a handbill (ca. 1924). Invitations extended to Jesse Bankston include inauguration ceremonies of presidents Jimmy Carter (1977) and Bill Clinton (1993), and Governor Kathleen Blanco of Louisiana (Jan. 2004). Also found in this group are Christmas cards sent by Governor Earl K. Long (ca. 1950, ca. 1957), and President Carter and Vice-President Mondale (1977-ca. 1979). Programs for the Capitol Correspondents Association Gridiron Show parody political figures, including Jesse Bankston (1960). Subseries 2. Published Material, 1936-2010, undated.. Published material includes books, serials, and newspaper clippings. The book, booklet attempts made by Governor Jimmie Davis and the Louisiana Legislature to circumvent a federal desegregation order (1960). An issue of the administration of Governor Sam Houston Jones (Oct. /Nov. 1971). senator\u2019s political achievements, and an issue of the Newspapers clippings report on political campaigns, political events, and the Louisiana Democratic Party. Series IV. Photographs, ca. 1930s-2005, undated. This series contains portraits, group photographs, and snapshots, with group photographs making up a large part of this series. Among the earliest in the series are group photographs of Bankston family members (ca. 1930s-ca. 1957). The remaining images show politicians and members of the Democratic Party at political events. Photographs of Jesse Bankston include portraits and snapshots, and photographs taken by the press when he served as the Director of the State Hospital (1951), shortly after his dismissal in 1959, and when he served on the State Board of Education. This series also includes photographs of Bill and Hillary Clinton (1992), Jimmy Carter (1976), Edwin Edwards (ca. 1970s), and General Troy Middleton (ca. 1970-1975). Series V. Personal Papers, 1933-1952, undated. This small group is comprised of social invitations, dance cards, Jesse Bankston\u2019s LSU diploma (1936), his employment history, and an agreement for improving the drainage on his subdivision lot in Baton Rouge (1952).'),
                 ],
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf':
                [('BIOGRAPHICAL/HISTORICAL NOTE', 'SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', u'William Acy, Jr., born in 1822, was a plantation owner in Tangipahoa Parish, Louisiana. He also served as Justice of the Peace of Ascension Parish, La. from 1885-1891. His father, William Acy, Sr., of the "Acey" family, emigrated from Hull, England, to the United States in the early 19th century. He lived in Baltimore, Maryland, then moved to General Wade Hampton\'s Millwood Plantation in South Carolina, and finally to Gen. Hampton\'s Point Houmas Plantation in Louisiana. William Acy, Jr. owned land in Louisiana and Mississippi, which included Standley Plantation in Carroll County, Mississippi. He married Margaret E. Stansbury in 1847, and after her death, he married Mrs. Mary Elizabeth Marchbanks Stevens, a widow, in 1865. He had one son, C. C. Acy. Among William Acy\u2019s most prominent acquaintances was Francis T. Nicholls, who served as Governor of Louisiana and Chief Justice of the Louisiana State Supreme Court.'),
                 ('SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'INDEX TERMS',
                  u"Correspondence, legal, and financial papers of William Acy, Jr., comprise this collection. Personal papers consist primarily of correspondence with relatives and friends in Maryland and England. They relate personal news and social activities, and provide some genealogical information. Among them is a letter from a cousin reporting on the poor living conditions in England and apathy of the people (Aug. 15, 1873). Business correspondence provides legal advice from Acy\u2019s attorneys and friends. Correspondence of Francis T. Nicholls pertains to Acy's properties (1888-1892). Letters from T. H. Somerville concern Standley Plantation, in Greenwood, Mississippi (1898-1901), and those of R. N. Sims concern a law suit before the Louisiana Supreme Court (1872). Letters from his son, C. C. Acy, describe conditions and management problems at Standley Plantation. There is also a letter from a patient confined to Jackson State Hospital complaining of conditions and inquiring about the length of his stay at the facility (April 15, 1907). He also questions whether he may have been committed for political reasons. Additionally, there are numerous letters regarding litigation over the settlement of the estate of William Acy, Sr., who died in 1882. Approximately $40,000 was owed to him at his death along with possible rights to property in Louisiana and Mississippi. There are numerous copies of court records kept by Acy, Jr., documenting the progression of a lawsuit filed against him by his nephew, William B. Lynam, who claimed a share in the estate of William Acy, Sr. Other documents include commissions signed by Louisiana Governors Hebert, Wickliffe and Moore confirming Acy, Jr.'s election as Justice of the Peace of Ascension Parish (1855-1861); a petition to the court submitted by James H. Muse against William Acy, Jr., for slander (Dec. 21, 1882); and a certificate awarded to Acy by the Amite City Lodge, No. 175 of the Louisiana Grand Lodge of Freemasons (March 4, 1871). Other legal papers consist of deeds and documents regarding property Acy acquired in Louisiana and Mississippi; papers pertaining to the estates of William Acy, Sr. and Margaret Stansbury Acy; and a sample ballot for the State and Tangipahoa Parish election of 1900. Canceled checks, tax receipts, bills, and invoices comprise the financial paper. Printed materials consist of maps of Baltimore, Maryland (1901) and London (undated); a legal brief submitted to the Louisiana Supreme Court in the case of (1882); advertising handbills, broadsides, pamphlets, catalogs, and books pertaining to railway travel (1897, 1901, 1907, 1908); hypnosis (1898); treatment of disease; sale of books, baby carriages, and farm equipment, including a cotton gin (1898). Among the medical printed materials is (1901) and prominent Southerners on the success of treatments. Additional printed volumes include the (April 1889, 1894, 1899, 1900). Photographs include cartes des visites, a cabinet card and a tintype, mostly of unidentified individuals. Photographs of family members include Elizabeth Stansbury Acy (1859), Mary Elizabeth Marchbanks Stevens Acy (1887), and William Acy, Sr. (1856). Bank books (1866- 1883, 1897-1902), memorandum books (1877-1903) and record books (1850-1899) comprise the manuscript volumes."),
                 ('LIST OF SERIES AND SUBSERIES',
                  'SERIES DESCRIPTIONS', 'INDEX TERMS', ''),
                 ('SERIES DESCRIPTIONS', 'INDEX TERMS', 'CONTAINER LIST', ''),
                 ],
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf':
                [('BIOGRAPHICAL/HISTORICAL NOTE', 'SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'Lewis Guion, the son of a sugar planter, was a jurist of Lafourche Parish, Louisiana. He studied law at the University of Virginia and practiced law in Thibodaux and New Orleans, Louisiana. On March 12, 1862, Guion enlisted as an officer in Company H of the 26th Louisiana Infantry Regiment under the leadership of Colonel Duncan S. Cage. After the Civil War, Guion established a sugar planting partnership with his brother-in- law, Francis T. Nicholls.'),
                 ('SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'INDEX TERMS',
                  "The diary describes Guion's departure from New Orleans (Apr. 24, 1862), his Company's march from Camp Moore to Donaldsonville, Baton Rouge, and Greensburg (May 4, 1862), and military activities around Chickasaw Bayou and Yazoo Lake (Dec. 24-29, 1862). Entries after May 18, 1863 give a daily account of the Siege of Vicksburg and events following the siege. Entries describe routine activities, the receipt of Northern and Southern newspapers by the besieged, the arrival of couriers from Johnston's army, camp food, and daily rations. The diary lists names and gives total numbers of daily casualties during the siege, recording information about individuals killed."),
                 ('LIST OF SERIES AND SUBSERIES',
                  'SERIES DESCRIPTIONS', 'INDEX TERMS', ''),
                 ('SERIES DESCRIPTIONS', 'INDEX TERMS', 'CONTAINER LIST', ''),
                 ],
            'http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf':
                [('BIOGRAPHICAL/HISTORICAL NOTE', 'SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'The Turnbull and Bowman families were cotton and sugar planters of West Feliciana Parish, Louisiana. John Turnbull and his brother, Walter, came to Louisiana from England in the 1770s. From their base in Louisiana, they traded furs, provisions, slaves, livestock, and agricultural produce including indigo and tobacco as partners in the firms Turnbull & Co., Turnbulls & Frazer, Turnbulls & Hood & Co., and Turnbull & Joyce. These companies traded goods in New Orleans, Natchez, Mobile, Pensacola, and London. They purchased pelts and skins from a number of Native Americans, probably of the Chickasaw and Choctaw tribes. The Turnbulls were involved in the slave trade and may have brought slaves to Louisiana from Jamaica and the West Indies. Traders and merchants from Louisiana and England who were associated with the Turnbulls included John Joyce (d. 1798), John Reid, David Hodge, David Ross, Walter Hood, Alexander Frazer (d. ca. 1791), James Frazer, James Montgomery, James Fletcher, Eslava, and others. John Joyce was an Englishman who fought in Canada during the American Revolution on the side of the British. He traded furs, slaves, and goods in Mississippi, Louisiana, Florida, and Alabama. Joyce owned Magnolia Mound Plantation, in Baton Rouge, Louisiana, from 1791 until his death in 1798. Walter Turnbull resided in Nassau where he owned a cotton plantation and lived with his wife, Mary, his son, John, and at least two daughters. By the 19th century, John Turnbull shifted his financial interests to planting and settled with his wife, Catherine (nee Rucker), and their children in Bayou Sara, West Feliciana Parish, Louisiana. Their children were John, Daniel (1796-1861), James F. (d. before 1831), Susannah (d. before 1831), Isabella (married Robert Semple), Sarah (married Lewis Stirling), and Walter (d. ca. 1838). Catherine managed many of her own business affairs; she jointly owned a plantation in St. Mary Parish with her son-in-law, John Towles, and had a house in New Orleans which she rented to Charles Norwood, a relative by marriage. She tutored children of planters and business people including Charles Norwood and Alexander Stirling. Daniel Turnbull (1796-1861) became a successful planter, primarily owning cotton plantations. In 1835, he founded Rosedown Plantation where he resided with his wife, Martha Hilliard Barrow Turnbull (1809-1896). Martha was raised on Highland Plantation in West Feliciana Parish. An avid horticulturist, she assembled a large collection of botanical specimens which she planted in extensive gardens at Rosedown. Children of this marriage included James Daniel (1836-1843), Daniel, William B. (1829-1856), and Sarah (1831-1914). In addition to Rosedown, Daniel operated Styopa, Catalpa, Middleplace, Hazelwood, Grove, Inheritance, Woodlawn, and De Soto plantations. Daniel Turnbull sold cotton through factors in New Orleans, including his nephew, A. M. Turnbull, who was member of the factorage A. M. Turnbull & Co. James F. Turnbull, under the name D. & J. Turnbull. James died before 1831. Daniel\' s son, William B. Turnbull, resided on De Soto Plantation in Bayou Sara. When he died (1856), William was survived by his wife, Caroline B. Turnbull (called "Caro"). Daniel Turnbull was the administrator of his estate. The Bowman and Turnbull families were associated through the marriage of Daniel and Martha\' s daughter, Sarah, to James P. Bowman (1832-1927). James was the son of Eliza Pirrie and her second husband, William R. Bowman (1800-1835), rector of Grace Episcopal Church in St. Francisville. Eliza Pirrie was the daughter of Lucretia (Lucy) Alston (1772- 1833) and James Pirrie (1769-1824). James, Lucy\' s second husband, served as alcalde under the Spanish governor Carlos de Grand-Pre. Eliza was raised at Oakley Plantation, which was founded by Ruffin Gray, the first husband of Lucy Alston. Ruffin Gray had moved to Louisiana from Virginia around 1770 when he received a Spanish land grant. In 1779, Ruffin was appointed alcalde in the Homochitto District by Manuel Gayoso de Lemos. Gray family members included Edmund (d. prior to 1777?), and Philip A., an attorney. Lucy and Ruffin had two children who survived to adulthood: Ruffin, Jr. (1796-1817), and Mary Anna Gray. Eliza was the only child of Lucy and James Pirrie to reach adulthood. From her family, Eliza inherited Oakley, Home, Ogden, and Prospect plantations. Eliza\' s first marriage was to her cousin, Robert Hilliard Barrow (1795-1823), of Greenwood Plantation. With Robert, Eliza resided at Prospect Plantation and had one son, Robert Hilliard Barrow, Jr. The marriage of Eliza to her second husband, William R. Bowman, produced two children: Isabelle Bowman and James Pirrie Bowman (1832-1927). In 1840, Eliza married her last husband, Henry E. Lyons, a lawyer from Philadelphia. Their three children were Cora, Lucie, and Eliza. Lyons became a partner in a law practice with F. A. Boyle of West Feliciana Parish. In the 1850s, Henry Lyons traveled to California where he speculated in real estate and other financial ventures. He lived in San Francisco and became one of three men to serve on the first Supreme Court of California. Sarah Turnbull inherited Rosedown and other plantations from her family. Like her mother, Sarah was a horticulturist. Her husband, James P. Bowman, produced cotton and sugar on Frogmoor and Bayou Grosse Tete plantations which he owned in Pointe Coupee Parish. In the 1890s, James was appointed to the Board of Administrators of the Insane Asylum of the State of Louisiana. He also served on the West Feliciana Parish School Board during the early 1900s. Upon her death in 1914, Sarah T. Bowman left her plantations and assets to her four daughters, Corrie (1872-1929), Isabel (1876-1951), Sarah (1869-1952), and Nina (1869-1955). In 1956, after the death of the last Bowman sister, the Rosedown Plantation home and gardens were purchased and restored by Milton and Catherine Underwood.'),
                 ('SCOPE AND CONTENT NOTE', 'LIST OF SERIES AND SUBSERIES', 'INDEX TERMS',
                  'Financial papers, correspondence, legal documents, personal papers, sheet music, printed items, and photographs covering the period 1771 to 1956 document lives of members of the Turnbull and Bowman families, cotton and sugar planters of West Feliciana Parish, Louisiana. Some papers of the related Pirrie and Gray families are included. The largest series of the collection consists of financial papers which chiefly reflect activities of the Turnbull and Bowman families as planters in Louisiana from the early 1800s into the 20th century. These include early documents pertaining to John and Walter Turnbull and their business concerns as traders of furs, slaves, horses, indigo, and produce in Louisiana, Mississippi, and the West Florida region. Correspondence reflects subjects documented by the financial papers including the colonial fur trade, planting, and economic conditions in Louisiana. Some personal family letters relate to social events, religion, education, and domestic matters. Legal documents chiefly relate to the Bowman, Pirrie, and Gray families but include Turnbull family legal agreements and suits. Some documents relate to activities of Ruffin Gray and James Pirrie as alcaldes during the Spanish governance of Louisiana. Of special note in the plantation and personal papers are lists of slaves and lists of plants purchased. Music and other printed items were collected by members of the Turnbull, Bowman and related families. Photographs primarily depict members of the Bowman family and Rosedown Plantation. In addition to Rosedown Plantation, the papers document Oakley, Middleplace, Hazelwood, Homochitto, Grosse Tete, Catalpa, Styopa, Inheritance, De Soto, Grove, Frogmoor, Prospect, and Home plantations.'),
                 ('LIST OF SERIES AND SUBSERIES', 'SERIES DESCRIPTIONS', 'INDEX TERMS',
                  'I. Financial papers Subseries 1. Turnbull family Subseries 2. Bowman and related families folders 3-4) II. Correspondence III. Legal documents IV. Plantation and personal papers V. Manuscript volumes VI. Music VII. Printed items VIII. Photographic materials I. Financial Papers Subseries 1. Turnbull family Summary: fur, indigo, slave, and livestock trade in colonial Louisiana. Papers of plantations managed by John and Catherine Turnbull, Daniel and Martha Turnbull, and William B. and James Turnbull. Early papers of John and Walter Turnbull relate to their business concerns as traders of furs, slaves, horses, indigo, and produce in Louisiana, Mississippi, and the West Florida region. Papers document accounts of Turnbull & Co. and the other companies in which John and Walter Turnbull had interests. Statements of the Turnbulls\' accounts in London with William Wilton and others were sent to Walter Turnbull in Nassau, who then forwarded copies to John Turnbull in the "Chickasaw Nation", in Mobile, and in Louisiana. Statements (1779-1804, some oversize) list pelts and other goods bought from traders in the region and from Native Americans. Papers record debts and credits of various companies and individuals who traded with the Turnbulls, notably John Joyce, William Wilton, David Hodge, David Ross, Alexander and James Frazer, Walter Hood, James Montgomery, and James Fletcher. Later financial papers (1785-1829, bulk 1808-1826) of John Turnbull and his wife, Catherine, document their activities as planters in Bayou Sara, West Feliciana Parish. Among the financial records of John Turnbull are receipts from Lardner Clark, a Nashville merchant (1789-1790), tuition receipts for children of Charles Norwood (1806-1807), a receipt from Charles Tessier for copying a last will and testament (1818); steamer bills of lading (1824), and general receipts for goods, services, and personal debts and credits. Financial papers of Catherine Turnbull include statements of her accounts with the New Orleans cotton factors Nathaniel Cox and Bartle & Cox (1811-1816). These statements document cotton sold by Catherine and comment on economic conditions; some (1816) mention arrangements for the education of Catherine\' s son, Walter, in New Orleans. Catherine\' s other receipts and statements document medical expenses of family members and slaves (1809-1825); salaries paid to plantation overseers (1809-1825); purchases of goods and services (1803-1829, undated); rental of a house in New Orleans (1808); payments for work as a tutor (1805, 1810, 1812, 1820); tax payments (1816); and shipments of goods on steamers (1818-1824). Receipts of Walter Turnbull (1805-1819), Charles Norwood (1790-1804), Henry Stirling (1827), and John Turnbull, [Jr.?] (1826) are included. receipts (for index of cotton factors, see Appendix A) which record sales of cotton in New Orleans and Liverpool. Letters discuss weather and crop conditions, political events, diseases and epidemics, ginning techniques, and other conditions affecting the quality of produce and market prices. Statements record purchases and offerings of manufactured goods, commodities, and slaves. Included are issues of the New Orleans Price-Current Commercial Intelligencer (1841, 1852). Other bills and receipts of Daniel Turnbull document purchases of goods from merchants, including Wm. Prince & Sons, a New York nursery supplier (for index of merchants, see Appendix B); legal services (1820-1856); medical and dental services for family, laborers, and slaves (1821-1875); personal debts and credits (1819-1860); the transport of passengers and goods aboard steamers (1821-1861); pew rental at the Grace Episcopal Church in St. Francisville (1854, 1859); and payments of taxes (1828-1859). Receipts (1825- 1860) for payments to overseers and other employees of Daniel Turnbull reflect their salaries and expenses. Financial papers of Daniel\' s wife, Martha, consist of cotton factors\' statements (1868-1872, see Appendix A) and receipts and bills for goods and services (1842-1877). Included is a statement of accounts, expenses, and credits (1867-1873) for Martha H. Turnbull and James P. Bowman. Papers document joint plantation management expenses of Daniel and his brother, James F. Turnbull (1823-1826), with statements of James\' account with cotton factor Nathaniel Cox (1825-1826). Statements, bills and receipts for goods and services reflect purchases by James F. Turnbull (1819-1827), William B. Turnbull (1853-1858, son of Daniel Turnbull), and William\' s widow, Caro B. Turnbull (1858, see Appendix B). Subseries 2. Bowman and related families Summary: and Bowman families. Bowman family items document management of plantations by Eliza B. Lyons, William R. Bowman, James P. Bowman, and Sarah T. Bowman. Some items document activities of Henry A. Lyons, Barrow family members, William Wilson Matthews, and others. Items pertaining to the Gray and Pirrie families include receipts for goods and services purchased by Ruffin Gray (1792-1795); Phil A. Gray (1808-1810, undated); and Edmund Gray (1776, oversized document). Financial papers of James Pirrie include statements (some oversize) and letters from cotton factors Flower & Faulkner (1809-1815), and its successor, Flower & Finley (1815-1816) of New Orleans. Letters discuss crop conditions, shipping, domestic and foreign politics, and market prices. James Pirrie\' s financial papers include records of expenses of plantation overseers (1811-1818); two unbound account books (1810- (1811-1821); sight drafts and receipts for personal debts and credits ([1801]-1823); and bills, receipts, and statements for purchases of goods and services (1804-1825). Financial papers of Eliza Bowman Lyons contain statements (1835-1849) from cotton factors Burke Watt & Co. and G. Burke & Co. which record sales of cotton, sugar, and molasses produced on Oakley and other plantations. Included are letters (1836-1837) from Burke, Watt & Co. to A. Skillman who helped manage the plantation interests of Eliza after the death of her second husband, William R. Bowman. Steamer receipts (1848-1851) record shipments of cotton from Home and Oakley plantations. Other papers (1825-1854, some oversize) include tax receipts (1828-1847); receipts documenting work on Oakley, Prospect, Home, and Ogden plantations; invoices of goods purchased; and sight drafts and receipts for personal debts and credits. William R. Bowman\' s statements from cotton factor Nathaniel Cox (1829-1835) concern cotton prices, William Bowman\' s health, and the transport of a boy "Alfred" to West Africa by the Sierlion (sic Sierra Leone) Colonization Society. His general receipts and statements (1829-1836, some oversize) include medical bills and receipts for payments to overseers (March 13, 1829; Apr. 30, 1833). Financial papers of Henry A. Lyons, Eliza\' s third husband, consist of sight drafts and receipts (1837-1849) for personal debts and credits, statements (1841-1856) for goods and services purchased, and a notice issued by a San Francisco bank (1853). Financial papers (1822-1860) of Barrow family members, Isabelle Bowman Matthews and William Wilson Matthews are included. Financial papers of James P. and Sarah T. Bowman contain statements from cotton factors and commission merchants (see Appendix A), with issues of the New Orleans Price-Current (1854, 1872). Other financial papers consist of mortgage documents (1910-1938), with a questionnaire (1922) from the U.S. Census Bureau concerning mortgages and tenants on farms; insurance papers (1911-1946); letters from bankers (1909-1922), with samples of checks and statements from various accounts (1908-1927); tax receipts (1866-1939); and bills and receipts for goods and services documenting plantation and personal expenses (see Appendix B). Other items document oats shipped to clients by James P. Bowman (1909- 1923); medical expenses (1877-1920); payments (1900-1912) to local newspapers for subscriptions and advertisements; items (1862-1863) recording work done by A. Heise on Frogmoor Plantation; miscellaneous Bowman financial papers (1821-1840); and unidentified bills and receipts (1780-1900). Summary: families. Correspondence of John and Walter Turnbull discusses their interests in colonial trade. Some Turnbull, Bowman, Pirrie, and Gray family letters relate to planting, religion, education, civic involvement, and social activities. The earliest correspondence in the collection consists of letters (1783-1811) to John Turnbull concerning his interests in colonial trade. These letters are from John Reid, David Hodge, David Ross, John Joyce, and others. Letters discuss political and economic conditions, the quality of furs, indigo, and other goods, the delivery of horses to Pensacola from the Chickasaw Nation (1786), sales of peltry in Louisiana, and a proposal to import slaves from Jamaica through a Spanish agent (1784). One letter (1792) from James Robertson (1742- 1814), pioneer and founder of Nashville (originally called Nash Borough), concerns a Creek Indian uprising near Nashville. Letters (1785-1796) by Walter Turnbull in Nassau and Long Island are addressed to John Turnbull in the Chickasaw Nation, New Orleans, and Mobile. They include copies of correspondence received by Walter from agents in London, chiefly William Wilton. Walter\' s letters discuss cotton planting in Nassau and encourage John Turnbull and John Joyce to purchase land there. Letters (1799-1805) from Walter\' s wife, Mary, are included with one letter (1799) from James Fletcher to Walter Turnbull. Letters (1799-1814) to Catherine Turnbull concern social matters and the education of her sons Walter, Daniel, and John. Letters (1823-1860) to Daniel Turnbull discuss his planting and business interests and include a letter of condolence from Leonidas Polk (1856) upon the death of a son. Also present are letters (1824, 1837) to James F. Turnbull and Martha Turnbull, correspondence (1797-1802) of family friends John Bisland and Charles Norwood, and unidentified letters (1786-1850, undated). Correspondence of the Pirrie and Gray families includes letters to James Pirrie (1808-1821) concerning financial and personal matters, a letter from Philip A. Gray about the sale of a slave, a personal letter to Lucy Pirrie from Mrs. L. Shipp (undated), and letters (1814-1815) from Ruffin Gray, Jr. to his parents describing his experiences at school in Lexington, Kentucky. Letters (1836-1849) to Eliza B. Lyons contain personal news and financial and legal advice on plantation management, with a letter from A. Skillman. Letters addressed to William R. Bowman from his father, Jacob, in Philadelphia discuss family and business concerns, the Episcopal Church, and religion. Other letters (1827-1833) to William discuss prices of sugar mills, the design and use of a corn sheller, purchases of plants from Philadelphia, the sale of a parcel of land, the hiring out of slaves, and legal opinions on paraphernal property. Letters (1840-1860) of Robert H. Barrow, Jr. and family concern personal matters and include letters (1860). Letters (1853-1870) from Robert H. Barrow, Jr. to James P. Bowman mention plantation affairs, shipments of cotton, and irrigation canals. Letters to Henry A. Lyons (1850-1854) from James P. Bowman and others concern the settlement of Eliza B. Lyons\' estate, the disposition of slaves belonging to Eliza, Lyons\' financial interests, and the construction of a railroad linking Baton Rouge with Bayou Grosse Tete. Included is a letter (1850) to E. H. Hodge concerning a bill in the California Senate and a letter (undated) from Lyons to his daughter, Cora. Letters (1900-1921) to James P. Bowman from his son, James P. Bowman, Jr., relate to plantation matters and the shooting of an African American youth by neighbors (1906). Letters from Bowman\' s daughter, Eliza, his son-in-law, George P. Shotwell (1897-1922), and his nephew, R. Bowman Matthews, are included. Other letters reflect James P. Bowman\' s involvement with the West Feliciana Parish School Board; the building of Julius Freyhan Memorial School (1905-1907); Bowman\' s appointment to the Board of Administrators of the Insane Asylum of the State of Louisiana (1899-1907); cotton and sugar growing on Grosse Tete and Frogmoor plantations (1855-1858), with letters from overseer George W. Woodruff; and the health of members of the Bowman family. The series contains an unidentified letter (1841) discussing allegations of misconduct of an overseer on Oakley Plantation and letters (1851-1956) to other Bowman family members. III. Legal documents Summary: Includes Turnbull family legal agreements and suits; documents related to activities of Ruffin Gray and James Pirrie as alcaldes under Spanish governance of Louisiana; and land titles, mortgages, and oil leases of the Bowman family. Legal documents (some in Spanish and French) primarily document interests of the Pirrie, Gray, and Bowman families but include agreements (1791, 1795) of John Turnbull and Michael Stoner and suits (1855, 1878) of Martha and Daniel Turnbull. Legal papers of the Gray family pertain to Edmund, Philip A., Ruffin, and Lucy Gray. Documents include an item appointing Edmund Gray as attorney for Bernard Rowmans (1771); items related to the settlement of estates of Edmund and Ruffin Gray; the appointment of Ruffin Gray as alcalde of the Homochitto District, signed by Manuel Gayoso de Lemos (1797); and deeds, titles, and transfers of land, slaves, and other property. James Pirrie\' s legal documents chiefly reflect his role as alcalde under the Spanish Commandant, Charles de Grand-Pre. Items (1804-1814) signed or witnessed by James Pirrie (some signed by Grand-Pre) include succession documents, an order for road repairs, transmittals of land and slaves, an allegation of crimes documents relate to land titles held by James and Lucy Pirrie. Bowman family documents relate to land titles, indebtedness of the estate of Nathaniel Cox to the estate of William R. Bowman (1837), the repair of roads by laborers of William R. Bowman (183-), legal fees for the succession of Sarah T. Bowman (1921), mortgages of property by Sarah T. and James P. Bowman (1895, 1922), and oil leases (1922). Miscellaneous legal documents (1803-1830, undated) relate to a suit concerning a horse race (1807), land disputes and transfers, and an appeal of a charge of burglary. IV. Plantation and personal papers Plantation papers include lists of slaves on Frogmoor and other plantations ([1815]-1861, undated), diary entries (1858) of work done on Frogmoor Plantation, and memoranda by James P. Bowman concerning plantation management (1875-1919). Planting and horticultural interests of William R. Bowman and others are documented by lists of plants purchased (1832, undated, also see letters and statements, 1834-1840, to Daniel Turnbull from Wm. Prince & Sons, a New York nursery supplier). Included are a drawing of a garden plan and memoranda recording cultivated lands. Personal papers consist of political resolutions (1875, undated) of the "Property Holders Protective Union," a group formed to oppose real estate tax rates in West Feliciana Parish; educational materials (1839-1840, undated) including historical essays and notes, foreign language lessons, and student writings; sermons by William R. Bowman (undated); certificates (oversize) appointing James P. Bowman to the Board of Administrators of the Insane Asylum of the State of Louisiana (1899) and to the West Feliciana Parish School Board (1904-1918); poetry; recipes and remedies; a guest list of visitors to Rosedown Plantation (1935-1946); and household memoranda. The series contains botanical specimens (1851, 1888-1901 undated, mostly European alpine plants) collected and mounted on paper by Sarah T. Bowman and others. V. Manuscript volumes Volumes contain records of crops produced, statements of account, lists of renters on plantations, records of hours worked by laborers, and plantation and household memoranda. The earliest volume (1793-1798) is a ledger containing accounts of John Turnbull. Other ledgers (1871-1935, kept chiefly by James P. Bowman) contain accounts of sales and purchases and records of cotton and other crops grown on Rosedown, Inheritance, and Hazelwood plantations. Some ledgers and volumes list renters on these plantations. Smaller volumes (1840-1921) were kept by Daniel and Martha Turnbull, James P. and Sarah T. Canal Bank with memoranda; time books recording work by laborers; James P. Bowman\' s record books containing plantation accounts and memoranda; and other memoranda books containing renters\' accounts, records of crops, household expenses, and miscellaneous entries. One volume contains notes on gardening (1919). Also included are students\' copy books (1838-1888), grade books, and a scrapbook. VI. Music Printed music was collected chiefly by members of the Bowman family and by Rosina Benoist, a relative. Manuscript music was created by Rosina Benoist and others. Bound volumes contain printed and manuscript music. Arranged by publisher, the printed sheet music was primarily issued by publishers in New York, Philadelphia, Baltimore, Boston, New Orleans, St. Louis, and other Midwestern towns (see Appendix C for list of sheet music publishers). VII. Printed items Includes circular letters, invitations, death notices, playbills, musical and theatrical programs, agricultural catalogs, advertisements, newspaper clippings, calling cards, greeting cards, postcards, games, plantation scrip, and other ephemera. Among the miscellaneous printed items are a compilation (1848) of statistics of Lowell manufacturers and a democratic ticket (undated). Oversize materials consist chiefly of broadsides and maps and include a democratic ticket (undated) and a steamer announcement (1848). VIII. Photographic materials Photographs (one oversized) consist of portraits and snapshots of members of the Bowman and related families. Included are images of Rosedown Plantation, Grace Episcopal Church in St. Francisville, and grave markers of family members.'),
                 ('SERIES DESCRIPTIONS', 'INDEX TERMS', 'CONTAINER LIST', ''),
                 ],
        }

        current_pdf_expected_answers = expected_answers[self.url]
        for our_tuple in current_pdf_expected_answers:
            firstheader, secondheader, backupheader, expected_result = our_tuple
            actual_result = self.findaid.getalltext(
                firstheader, secondheader, backupheader)
            actual_result_formatted, expected_result_formatted = actual_result.encode(
                'ascii', 'ignore'), expected_result.encode('ascii', 'ignore')
            self.assertEquals(actual_result, expected_result, '\n\nFor url :{}\nHeaders: {}, {}, {}\nExpected return value: {}\nActual return value: {}\n'.format(
                self.url, firstheader, secondheader, backupheader, expected_result_formatted, actual_result_formatted))

    def testSeriesSplit(self):
        almostListSeries = self.findaid.getalltext("LIST OF SERIES AND SUBSERIES", "SERIES DESCRIPTIONS", "INDEX TERMS")
        seriesdesc       = self.findaid.getalltext("SERIES DESCRIPTIONS", "INDEX TERMS", "CONTAINER LIST")
        finalseries      = self.findaid.seriesSplit(almostListSeries, "list", "head", "item", False)
        seriesdesc       = self.findaid.seriesSplit(seriesdesc, "co1", "unitid", "p", True)
        # print(finalseries)

        #I feel like this test could be better named... also it's commented out so it always fails

    # def testGetDeflistItem(self):
    #     labels = [
    #         'Created by',
    #         'Compiled by',
    #         'Revised by',
    #         'Encoded by',
    #         'Processed by',
    #         'Date Completed'
    #     ]
    #     expected_answers = {
    #         'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf':
    #             [
    #                 ('Compiled by', 'Luana Henderson')
    #             ],
    #         'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0826.pdf':
    #             [
    #                 ('', '')
    #             ],
    #         'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf':
    #             [
    #                 ('Compiled by', 'Luana Henderson')
    #             ],
    #         'http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf': []
    #     }
    #     tuple_list = expected_answers[self.url]
    #     for our_tuple in tuple_list:

    #         label, value = our_tuple
    #         observed = self.findaid.getDefListItem(label)
    #         self.assertEquals(observed, value, 'For url: {}\nUnexpected Value for: {}\nGot: {}\nExpected: {}\n\n'.format(
    #             self.url, label, observed, value))


    #         #I'm starting to wonder what to do when we encounter a non <p> tag, should we just pass?
    #         #question: Do we need to populate expected text for every pdf?

    # def testGetTextAfterHeader(self):
    #     sample_header_and_pages = {'http://www.lib.lsu.edu/sites/default/files/sc/findaid/4452.pdf': (
    #         ('Biographical/Historical Note', (4, 4),
    #             """The Turnbull and Bowman families were cotton and sugar planters of West Feliciana Parish, Louisiana. John Turnbull and his brother, Walter, came to Louisiana from England in the 1770s. From their base in Louisiana, they traded furs, provisions, slaves, livestock, and agricultural produce including indigo and tobacco as partners in the firms Turnbull & Co., Turnbulls & Frazer, Turnbulls & Hood & Co., and Turnbull & Joyce. These companies traded goods in New Orleans, Natchez, Mobile, Pensacola, and London. They purchased pelts and skins from a number of Native Americans, probably of the Chickasaw and Choctaw tribes.  The Turnbulls were involved in the slave trade and may have brought slaves to Louisiana from Jamaica and the West Indies. Traders and merchants from Louisiana and England who were associated with the Turnbulls included John Joyce (d. 1798), John Reid, David Hodge, David Ross, Walter Hood, Alexander Frazer (d. ca. 1791), James Frazer, James Montgomery, James Fletcher, Eslava, and others. John Joyce was an Englishman who fought in Canada during the American Revolution on the side of the British. He traded furs, slaves, and goods in Mississippi, Louisiana, Florida, and Alabama. Joyce owned Magnolia Mound Plantation, in Baton Rouge, Louisiana, from 1791 until his death in 1798. Walter Turnbull resided in Nassau where he owned a cotton plantation and lived with his wife, Mary, his son, John, and at least two daughters.  By the 19th century, John Turnbull shifted his financial interests to planting and settled with his wife, Catherine (nee Rucker), and their children in Bayou Sara, West Feliciana Parish, Louisiana. Their children were John, Daniel (1796-1861), James F. (d. before 1831), Susannah (d. before 1831), Isabella (married Robert Semple), Sarah (married Lewis Stirling), and Walter (d. ca. 1838). Catherine managed many of her own business affairs; she jointly owned a plantation in St. Mary Parish with her son-in-law, John Towles, and had a house in New Orleans which she rented to Charles Norwood, a relative by marriage. She tutored children of planters and business people including Charles Norwood and Alexander Stirling.  Daniel Turnbull (1796-1861) became a successful planter, primarily owning cotton plantations.  In 1835, he founded Rosedown Plantation where he resided with his wife, Martha Hilliard Barrow Turnbull (1809-1896). Martha was raised on Highland Plantation in West Feliciana Parish. An avid horticulturist, she assembled a large collection of botanical specimens which she planted in extensive gardens at Rosedown. Children of this marriage included James Daniel (1836-1843), Daniel, William B. (1829-1856), and Sarah (1831-1914). In addition to Rosedown, Daniel operated Styopa, Catalpa, Middleplace, Hazelwood, Grove, Inheritance, Woodlawn, and De Soto plantations. Daniel Turnbull sold cotton through factors in New Orleans, including his nephew, A. M. Turnbull, who was member of the factorage A. M. Turnbull & Co.  In the 1820s, Daniel managed plantation property near St. Francisville jointly with his brother, James F. Turnbull, under the name D. & J. Turnbull. James died before 1831. Daniel' s son, William B. Turnbull, resided on De Soto Plantation in Bayou Sara. When he died (1856), William was survived by his wife, Caroline B. Turnbull (called "Caro"). Daniel Turnbull was the administrator of his estate.  The Bowman and Turnbull families were associated through the marriage of Daniel and Martha' s daughter, Sarah, to James P. Bowman (1832-1927). James was the son of Eliza Pirrie and her second husband, William R. Bowman (1800-1835), rector of Grace Episcopal Church in St. Francisville. Eliza Pirrie was the daughter of Lucretia (Lucy) Alston (1772-1833) and James Pirrie (1769-1824). James, Lucy' s second husband, served as alcalde under the Spanish governor Carlos de Grand-Pre. Eliza was raised at Oakley Plantation, which was founded by Ruffin Gray, the first husband of Lucy Alston. Ruffin Gray had moved to Louisiana from Virginia around 1770 when he received a Spanish land grant. In 1779, Ruffin was appointed alcalde in the Homochitto District by Manuel Gayoso de Lemos. Gray family members included Edmund (d. prior to 1777?), and Philip A., an attorney. Lucy and Ruffin had two children who survived to adulthood: Ruffin, Jr. (1796-1817), and Mary Anna Gray.  Eliza was the only child of Lucy and James Pirrie to reach adulthood. From her family, Eliza inherited Oakley, Home, Ogden, and Prospect plantations.  Eliza' s first marriage was to her cousin, Robert Hilliard Barrow (1795-1823), of Greenwood Plantation. With Robert, Eliza resided at Prospect Plantation and had one son, Robert Hilliard Barrow, Jr. The marriage of Eliza to her second husband, William R. Bowman, produced two children: Isabelle Bowman and James Pirrie Bowman (1832-1927). In 1840, Eliza married her last husband, Henry E. Lyons, a lawyer from Philadelphia. Their three children were Cora,Lucie, and Eliza. Lyons became a partner in a law practice with F. A. Boyle of West Feliciana Parish. In the 1850s, Henry Lyons traveled to California where he speculated in real estate and other financial ventures. He lived in San Francisco and became one of three men to serve on the first Supreme Court of California.  Sarah Turnbull inherited Rosedown and other plantations from her family. Like her mother, Sarah was a horticulturist. Her husband, James P. Bowman, produced cotton and sugar on Frogmoor and Bayou Grosse Tete plantations which he owned in Pointe Coupee Parish. In the 1890s, James was appointed to the Board of Administrators of the Insane Asylum of the State of Louisiana. He also served on the West Feliciana Parish School Board during the early 1900s. Upon her death in 1914, Sarah T. Bowman left her plantations and assets to her four daughters, Corrie (1872-1929), Isabel (1876-1951), Sarah (1869-1952), and Nina (1869-1955).  In 1956, after the death of the last Bowman sister, the Rosedown Plantation home and gardens were purchased and restored by Milton and Catherine Underwood."""
    #          ),
    #         ('Scope and Content Note', (6, 6),
    #             """Financial papers, correspondence, legal documents, personal papers, sheet music, printed items, and photographs covering the period 1771 to 1956 document lives of members of the Turnbull and Bowman families, cotton and sugar planters of West Feliciana Parish, Louisiana.  Some papers of the related Pirrie and Gray families are included. The largest series of the collection consists of financial papers which chiefly reflect activities of the Turnbull and Bowman families as planters in Louisiana from the early 1800s into the 20th century. These include early documents pertaining to John and Walter Turnbull and their business concerns as traders of furs, slaves, horses, indigo, and produce in Louisiana, Mississippi, and the West Florida region. Correspondence reflects subjects documented by the financial papers including the colonial fur trade, planting, and economic conditions in Louisiana. Some personal family letters relate to social events, religion, education, and domestic matters. Legal documents chiefly relate to the Bowman, Pirrie, and Gray families but include Turnbull family legal agreements and suits. Some documents relate to activities of Ruffin Gray and James Pirrie as alcaldes during the Spanish governance of Louisiana. Of special note in the plantation and personal papers are lists of slaves and lists of plants purchased. Music and other printed items were collected by members of the Turnbull, Bowman and related families. Photographs primarily depict members of the Bowman family and Rosedown Plantation. In addition to Rosedown Plantation, the papers document Oakley, Middleplace, Hazelwood, Homochitto, Grosse Tete, Catalpa, Styopa, Inheritance, De Soto, Grove, Frogmoor, Prospect, and Home plantations."""
    #          ),
    #         ('List of Series and Subseries', (7, 7), """   """),
    #         ('Series and Subseries Descriptions', (8, 8), """   """),
    #         ('Index Terms', (15, 15), """   """),
    #         ('Container List', (18, 18), """   """),
    #         ('Microfilm Container List', (21, 21), """   """),
    #         ('Appendices', (22, 22), """   """),
    #         ('B Index to Merchants', (23, 23), """   """),
    #         ('C List of Music Publishers', (24, 24), """   """),
    #     ),
    #     'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf': (
    #         ('Summary', (3, 3), """"""),
    #         ('Biographical/Historical Note', (4, 4), """Jesse Homer Bankston was born Oct. 7, 1907 to Allie Magee and Leon V. Bankston of Washington Parish, La. He was educated in local schools and received his Ruth Paine (1918&#8211;1997), daughter of Walter R. Paine, Sr. Ruth was a member of the Bankston began his career in government in 1940 under Governor As a management consultant, he was charged with the reorganization of state government. In 1942, he became an organizational specialist in the Louisiana Civil Service Department. Under Governor assistant in the Department of Institutions and later as the director of that same Department. The Department, which was created 1940 and re-organized in 1942, supervised all mental, tuberculosis, and general hospitals, together with the State Penitentiary and two institutions for delinquent youths. When Governor Earl K. Long left office in 1952, Bankston left state government to open a healthcare consulting firm. With Governor Long&#8217;s return to office in 1956, Bankston was appointed the director of the newly established Department of Hospitals. He held this position until the summer of 1959, when he was dismissed after a dispute over the governor&#8217;s mental health. After his dismissal, Bankston returned to his consulting firm, and began to work with Democratic Party candidates and issues. He also joined the boards of the newly established Louisiana Public Broadcasting, and State Board of Elementary and Secondary Education. Elected in 1968, he served on State Board of Elementary and Secondary Education for 28 years. During his tenure, he served as secretary and chairman of the Board. Bankston was also the longest serving member of the Louisiana Democratic State Central Committee, having served for 51 years until his death in 2010. In 2002, he was inducted into the Louisiana Political Hall of Fame. In addition to his political pursuits, he also served as president of the Baton Rouge YMCA, Young Men's Business Club, Mental Health Association, and Tuberculosis Society."""),
    #         ('Scope and Content Note', (5, 5), """The collection, consisting of correspondence, political files, printed items and photographs, reflects Jesse H. Bankston&#8217;s involvement in Louisiana state government and the Louisiana Democratic Party. Correspondence discusses political elections, candidates, and government health services. Political files pertain to activities of the Democratic Party, Louisiana politicians, and Louisiana Department of Institutions and State Hospital Board. Printed items contain ephemera and published material. Ephemera include programs, invitations, campaign buttons and bumper stickers, and items relating to the Mardi Gras celebration in Washington, D. C. Published material includes books, serials, newspaper clippings, and scrapbooks relating to Louisiana politics, campaigns and the National Democratic Convention of 1976. Photographs contain portraits, group photographs, and snapshots, with group photographs making up a large part of this series. Early photographs show several Bankston family members (ca. 1930s-ca. 1957). The remaining images show politicians and members of the Democratic Party at political events. The collection also includes a few miscellaneous personal papers."""),
    #         ('List of Series and Subseries', (6, 6), """   """),
    #         ('Series Descriptons', (7, 7), """   """),
    #         ('Index Terms', (10, 10), """   """),
    #         ('Container List', (18, 18), """   """),
    #     ),
    #     }
    #     if self.url not in sample_header_and_pages: 
    #         self.assertEquals(False, True, "Missing expected values information for {}".format(self.url))
    #     current_pdfs_expected_answer = sample_header_and_pages[self.url]

    #     for section, page_nums, expected_text in current_pdfs_expected_answer:
    #         observed_result = self.findaid.get_text_after_header(
    #             (section, page_nums))
    #     self.assertEquals(observed_result, expected_text, 'For url: {}\nUnexpected Value for: {}\nGot: {}\nExpected: {}\n\n'.format(
        
    #         self.url, section, observed_result, expected_text))


    def testCollapser(self):
        unit_0717 = '''<unit><text top="174" left="135" width="647" height="16" font="0"><a href="tmpqOHeUC.html#3">SUMMARY ........................................................................................................................ 3</a></text>
                <text top="170" left="782" width="4" height="21" font="2"> </text>
                <text top="195" left="135" width="647" height="16" font="0"><a href="tmpqOHeUC.html#4">BIOGRAPHICAL/HISTORICAL NOTE .......................................................................... 4</a></text>
                <text top="191" left="782" width="4" height="21" font="2"> </text>
                <text top="215" left="135" width="647" height="16" font="0"><a href="tmpqOHeUC.html#5">SCOPE AND CONTENT NOTE ....................................................................................... 5</a></text>
                <text top="212" left="782" width="4" height="21" font="2"> </text>
                <text top="236" left="135" width="647" height="16" font="0"><a href="tmpqOHeUC.html#6">LIST OF SERIES AND SUBSERIES ................................................................................ 6</a></text>
                <text top="232" left="782" width="4" height="21" font="2"> </text>
                <text top="257" left="135" width="647" height="16" font="0"><a href="tmpqOHeUC.html#7">SERIES DESCRIPTIONS .................................................................................................. 7</a></text>
                <text top="253" left="782" width="4" height="21" font="2"> </text>
                <text top="278" left="135" width="647" height="16" font="0"><a href="tmpqOHeUC.html#10">INDEX TERMS ................................................................................................................ 10</a></text>
                <text top="274" left="782" width="4" height="21" font="2"> </text>
                <text top="298" left="135" width="647" height="16" font="0"><a href="tmpqOHeUC.html#11">CONTAINER LIST .......................................................................................................... 11</a></text>
                </unit>'''
        unit = '''<unit>
                <text top="112" left="108" width="251" height="16" font="0"><b>ACY (WILLIAM) JR. PAPERS </b></text>
                <text top="106" left="360" width="5" height="24" font="1"> </text>
                <text top="106" left="459" width="5" height="24" font="1"> </text>
                <text top="112" left="707" width="108" height="16" font="0"><b>Mss. 717, 772 </b></text>
                <text top="127" left="108" width="82" height="24" font="1">1844-1909 </text>
                <text top="127" left="459" width="5" height="24" font="1"> </text>
                <text top="127" left="563" width="252" height="24" font="1">LSU Libraries Special Collections </text>
                <text top="1037" left="418" width="86" height="24" font="1">Page <b>2</b> of <b>9</b> </text>
                <text top="1058" left="108" width="5" height="24" font="1"> </text>
                <text top="190" left="108" width="248" height="16" font="0"><b>CONTENTS OF INVENTORY </b></text>
                <text top="205" left="108" width="5" height="24" font="1"> </text>
                <text top="225" left="108" width="5" height="24" font="1"> </text>
                <text top="246" left="162" width="75" height="24" font="1"><a href="tmpZROglH.html#3">Summary </a></text>
                <text top="246" left="270" width="5" height="24" font="1"><a href="tmpZROglH.html#3"> </a></text>
                <text top="246" left="324" width="5" height="24" font="1"><a href="tmpZROglH.html#3"> </a></text>
                <text top="246" left="378" width="5" height="24" font="1"><a href="tmpZROglH.html#3"> </a></text>
                <text top="246" left="432" width="5" height="24" font="1"><a href="tmpZROglH.html#3"> </a></text>
                <text top="246" left="486" width="5" height="24" font="1"><a href="tmpZROglH.html#3"> </a></text>
                <text top="246" left="540" width="5" height="24" font="1"><a href="tmpZROglH.html#3"> </a></text>
                <text top="246" left="594" width="5" height="24" font="1"><a href="tmpZROglH.html#3"> </a></text>
                <text top="246" left="648" width="14" height="24" font="1"><a href="tmpZROglH.html#3">3</a> </text>
                <text top="267" left="162" width="221" height="24" font="1"><a href="tmpZROglH.html#4">Biographical/Historical Note   </a></text>
                <text top="267" left="432" width="5" height="24" font="1"><a href="tmpZROglH.html#4"> </a></text>
                <text top="267" left="486" width="5" height="24" font="1"><a href="tmpZROglH.html#4"> </a></text>
                <text top="267" left="540" width="5" height="24" font="1"><a href="tmpZROglH.html#4"> </a></text>
                <text top="267" left="594" width="5" height="24" font="1"><a href="tmpZROglH.html#4"> </a></text>
                <text top="267" left="648" width="28" height="24" font="1"><a href="tmpZROglH.html#4">4-5 </a></text>
                <text top="288" left="162" width="180" height="24" font="1"><a href="tmpZROglH.html#5">Scope and Content Note </a></text>
                <text top="288" left="378" width="5" height="24" font="1"><a href="tmpZROglH.html#5"> </a></text>
                <text top="288" left="432" width="5" height="24" font="1"><a href="tmpZROglH.html#5"> </a></text>
                <text top="288" left="486" width="5" height="24" font="1"><a href="tmpZROglH.html#5"> </a></text>
                <text top="288" left="540" width="5" height="24" font="1"><a href="tmpZROglH.html#5"> </a></text>
                <text top="288" left="594" width="5" height="24" font="1"><a href="tmpZROglH.html#5"> </a></text>
                <text top="288" left="648" width="28" height="24" font="1"><a href="tmpZROglH.html#5">5-6 </a></text>
                <text top="288" left="702" width="5" height="24" font="1"> </text>
                <text top="308" left="162" width="113" height="24" font="1"><a href="tmpZROglH.html#7">Index Terms   </a></text>
                <text top="308" left="324" width="59" height="24" font="1"><a href="tmpZROglH.html#7">          </a></text>
                <text top="308" left="432" width="5" height="24" font="1"><a href="tmpZROglH.html#7"> </a></text>
                <text top="308" left="486" width="5" height="24" font="1"><a href="tmpZROglH.html#7"> </a></text>
                <text top="308" left="540" width="5" height="24" font="1"><a href="tmpZROglH.html#7"> </a></text>
                <text top="308" left="594" width="5" height="24" font="1"><a href="tmpZROglH.html#7"> </a></text>
                <text top="308" left="648" width="14" height="24" font="1"><a href="tmpZROglH.html#7">7 </a></text>
                <text top="329" left="162" width="113" height="24" font="1"><a href="tmpZROglH.html#8">Container List  </a></text>
                <text top="329" left="324" width="5" height="24" font="1"><a href="tmpZROglH.html#8"> </a></text>
                <text top="329" left="378" width="5" height="24" font="1"><a href="tmpZROglH.html#8"> </a></text>
                <text top="329" left="432" width="5" height="24" font="1"><a href="tmpZROglH.html#8"> </a></text>
                <text top="329" left="486" width="5" height="24" font="1"><a href="tmpZROglH.html#8"> </a></text>
                <text top="329" left="540" width="5" height="24" font="1"><a href="tmpZROglH.html#8"> </a></text>
                <text top="329" left="594" width="5" height="24" font="1"><a href="tmpZROglH.html#8"> </a></text>
                <text top="329" left="648" width="28" height="24" font="1"><a href="tmpZROglH.html#8">8-9 </a></text>
            </unit>'''
        tree = etree.fromstring(unit)
        path = '//text[b[contains(text(), "CONTENTS OF INVENTORY")]]/following-sibling::text/a'
        elms = tree.xpath(path)
        collapsed = self.findaid.collapse(elms)

    def testCollapseRealPdfs(self):
        contents = self.findaid.element_tree.xpath('//page/text[b[contains(text(), "CONTENTS OF INVENTORY")]]/following-sibling::text/a')

    # Unless our list of subject  terms is going to change we don't need this.
    #     #should take known Index Terms and add headers to terms.
    # def testAssembleSubjectTermsDictionary(self):


    def testget_first_page_siblings_and_children(self):
        fixture = '''<page>
            <text>Scope and Content Note</text>
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
        print ET.tostring(arch)

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
            print result
        else: 
            result = None

        for term in result:
            print self.findaid.which_subject_heading_type(term)
        #print result

   
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
