# original workflow -- for reference

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

        # all these items are found in the SUMMARY section. (not to be confused with 'Summary.')
        # sometimes there is a period sometimes not...
        pdfextent = self.getrcoldata("Size.") 
          = self.getrcoldata("Inclusive dates.")
        pdfbdates = self.getrcoldata("Bulk dates.")
        pdfuserestrict = self.getrcoldata("Copyright.")
        pdfprefercite = self.getrcoldata("Citation.")
        pdfabstract = self.getrcoldata("Summary.")

        pdflanguage = self.getrcoldata("Language.")
        if pdflanguage == "":
            pdflanguage = self.getrcoldata("Languages.")

        pdfaccessrestrict = self.getrcoldata("Restrictions on access.")
        if pdfaccessrestrict == "":
            pdfaccessrestrict = self.getrcoldata("Access restrictions.")

        pdfrelatedmaterial = self.getrcoldata("Related collections.")
        if pdfrelatedmaterial == "":
            pdfrelatedmaterial = self.getrcoldata("Related collection.")

        pdfphysloc = self.getrcoldata("Stack locations.")
        if pdfphysloc == "":
            pdfphysloc = self.getrcoldata("Stack location.")

        # Then the getalltext function won't need a backupheader, and we can get all text by looping through available terms for appropriate sections
        pdfbioghist = self.getalltext("BIOGRAPHICAL/HISTORICAL NOTE", "SCOPE AND CONTENT NOTE", "LIST OF SERIES AND SUBSERIES")
        pdfscopecontent = self.getalltext("SCOPE AND CONTENT NOTE", "LIST OF SERIES AND SUBSERIES", "INDEX TERMS")
        almostListSeries = self.getalltext("LIST OF SERIES AND SUBSERIES", "SERIES DESCRIPTIONS", "INDEX TERMS")
        seriesdesc = self.getalltext("SERIES DESCRIPTIONS", "INDEX TERMS", "CONTAINER LIST")
        # this is where series & subseries data is added to the xml
        seriesdesc = self.seriesSplit(seriesdesc, "co1", "unitid", "p", True)
        # finalseries = self.seriesSplit(almostListSeries, "list", "head", "item", False)

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
        # print etree.tostring(ead, pretty_print=True)
        # problem right now with ..... vs whitespace, getting some lists ['section pg'] others ['section', 'pg']
        # I think we solved this, yes?


        # If I understand this correctly, this pulls the Left Column data and Right Column data from SUMMMARY 

    def getrcoldata(self, lcolname):
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
