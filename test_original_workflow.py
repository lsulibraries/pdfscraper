
    # def testGetRColData(self):
    #     # size = self.findaid.getrcoldata('Size.')
    #     pass

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