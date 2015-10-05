#!/usr/bin/env python

# 1. Add some necessary libraries
import scraperwiki, urllib2
from lxml import etree
from lxml.builder import E
from collections import OrderedDict #for deduping lists while maintaining order
 
# 2. The URL/web address where we can find the PDF we want to scrape
pdfurl = 'http://www.lib.lsu.edu/sites/default/files/sc/findaid/5078.pdf' #Bankston
#pdfurl = 'http://www.lib.lsu.edu/sites/default/files/sc/findaid/0717.pdf' #Acy papers
#pdfurl = 'http://lib.lsu.edu/special/findaid/0826.pdf' #Guion Diary
#pdfurl = 'http://lib.lsu.edu/special/findaid/4452.pdf' #Turnbull - multiple page biographical note
 
# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(pdfurl).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
xmldata = bytes(bytearray(xmldata, encoding='utf-8'))
root = etree.fromstring(xmldata)

#print root
 
# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
#print etree.tostring(root, pretty_print=True)

#create variables for the elements, using xpath and other logic

#titleproper - needs to account for multiple lines in some docs
wholetitle =[]
titlelines = root.xpath('//page[@number="1"]/text[@top>="200" and @width>"10"]/b')
for el in titlelines:
    wholetitle.append(el.text.strip())
pdftitleproper = 'A GUIDE TO THE ' + ' '.join(wholetitle)
titlelineend = titlelines[-1].getparent().get('top') #figuring out what the top value of the last line of the title is

#num - assume it is between 12 and 25 units below the last line of title (a better way might have been to take next text node)
numlinenumberA = str(int(titlelineend) + 12)
numlinenumberB = str(int(titlelineend) + 25)
pdfnum = root.xpath('//page[@number="1"]/text[@top>=' + numlinenumberA + ' and @top<=' + numlinenumberB + ']')[0].text.strip()

#subtitle - will subtitle always be the same? - if so then hard-coding the value
pdfsubtitle = 'A Collection in the Louisiana and Lower Mississippi Valley Collections'

#author - take next text node after the one that says "Compiled by" - with exception handling
try:
    pdfauthor = root.xpath('//page[@number="1"]/text[text()[normalize-space(.)="Compiled by"]]')[0].getnext().text.strip()
except:
    pdfauthor = 'Special Collections Staff'
    
#publisher - assuming publisher can be hard-coded
pdfpublisher = 'Louisiana State University Special Collections'

#addressline
pdfaddressline1 = 'Hill Memorial Library'
pdfaddressline2 = 'Baton Rouge, LA 70803'
pdfaddressline3 = 'http://www.lib.lsu.edu/special'

#date - last node over "20" width on first page - "reformatted" or "revised" dates okay?
pdfdate = root.xpath('//page[@number="1"]/text[@width>"20"]')[-1].text.strip()

#head - always summary?
pdfhead = 'SUMMARY'

#physdesc - 

#page 3 has a table - find the left of the two columns - can assume Size is the first and always there?
leftcolumnleft = str(int(root.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="Size."]]')[0].getparent().get('left')))

#function finds right hand column data based on text of left hand column - just for page 3
def getrcoldata (lcolname):
    lcoldata = []
    #try it first as is, if not then try it again without the last character (usually a period)
    try:
        rcoltop = str(int(root.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolname + '"]]')[0].getparent().get('top')))
        rcoltopbuffer = str(int(rcoltop)-10)
        afterrcoltop = str(int(root.xpath('//page[@number="3"]/text[@left='+leftcolumnleft+' and @top=' + rcoltop + ']/following::text[b]')[0].get('top'))-10)
        if afterrcoltop < rcoltop: #check to see if it's last on page (it loops to top for some reason). if so hopefully one line is needed
            afterrcoltop = str(int(rcoltop)+20)
        datalines = root.xpath('//page[@number="3"]/text[@top>' + rcoltopbuffer + 'and @top<' + afterrcoltop + ' and @left>"200"]')
        for el in datalines:
            lcoldata.append(el.text.strip())
        pdfdata = ' '.join(lcoldata)
    except:
        try:
            lcolnameshort = lcolname[:-1]
            rcoltop = str(int(root.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolnameshort + '"]]')[0].getparent().get('top')))
            rcoltopbuffer = str(int(rcoltop)-10)
            try: #if it's the last in the column then hopefully its a single line
                afterrcoltop = str(int(root.xpath('//page[@number="3"]/text[@left='+leftcolumnleft+' and @top=' + rcoltop + ']/following::text[b]')[0].get('top'))-10)
            except:
                aftercoltop = str(int(rcoltop)+15)
            datalines = root.xpath('//page[@number="3"]/text[@top>' + rcoltopbuffer + 'and @top<' + afterrcoltop + ' and @left>"200"]')
            for el in datalines:
               lcoldata.append(el.text.strip())
            pdfdata = ' '.join(lcoldata)
        except:
            try: #split query - test each against different lines and expand the selection
                lcolnamefirstpart = lcolname.rsplit(' ',1)[0]
                lcolnamelastword = lcolname.rsplit(' ',1)[1]
                rcoltop = str(int(root.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolnamefirstpart + '"]]')[0].getparent().get('top')))
                rcoltopbuffer = str(int(rcoltop)-10)
                nextcoltop = str(int(root.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolnamelastword + '"]]')[0].getparent().get('top')))
                afterrcoltop = str(int(root.xpath('//page[@number="3"]/text[@left='+leftcolumnleft+' and @top=' + nextcoltop + ']/following::text[b]')[0].get('top'))-10)
                datalines = root.xpath('//page[@number="3"]/text[@top>' + rcoltopbuffer + 'and @top<' + afterrcoltop + ' and @left>"200"]')
                for el in datalines:
                    lcoldata.append(el.text.strip())
                pdfdata = ' '.join(lcoldata)
            except:
                pdfdata = ' '
    #strip first character of data if it's a period or space
    try:
        if pdfdata[0] == "." or pdfdata[0] == " ":
            pdfdata = pdfdata[1:]
    except: 
        pass
    try:
        nextboldtext = root.xpath('//page[@number="3"]/text/b[text()[normalize-space(.)="' + lcolname + '"]]')[0].getparent().getnext().getchildren()[0].text
        #print nextboldtext
    except:
        pass
    return pdfdata.strip()

#finds what page number a particular term appears on and what the "top" value is
def getpagenum (term):
    termtop = ""
    for pagenumber in range (4, 19):
        try:
            termtop = str(int(root.xpath('//page[@number='+str(pagenumber)+']/text/b[text()[normalize-space(.)="'+term+'"]]')[0].getparent().get('top')))
            break
        except:
            continue
    return pagenumber, termtop
   
#gets text nodes in between two headers
def getalltext(firstheader, secondheader, backupheader):
    firstpagenumber, firstheadertop = getpagenum(firstheader)
    secondpagenumber, secondheadertop = getpagenum(secondheader)
    backuppagenumber, backupheadertop = getpagenum(backupheader)
    if backuppagenumber < secondpagenumber or secondpagenumber == 19:
        secondpagenumber = backuppagenumber
        secondheadertop = backupheadertop
    rawtext = []
    for p in range (firstpagenumber, secondpagenumber+1):
        if p == secondpagenumber:
            bottom = secondheadertop
        else:
            bottom = "1000"
        #print firstheader, firstpagenumber, firstheadertop, secondpagenumber, bottom
        data = root.xpath('//page[@number='+str(p)+']/text[@top>=' + str(int(firstheadertop)+3) + 'and @top<' + str(int(bottom)-3) +']|//page[@number='+str(p)+']/text[@top>=' + str(int(firstheadertop)+3) + 'and @top<' + str(int(bottom)-3) +']/b')
        for el in data:
            if el.text == None :  #removes blank nodes
                continue
            rawtext.append(el.text.strip())
    textalmost = ' '.join(rawtext)
    alltext = ' '.join(textalmost.split()) #strips extra spaces
    return alltext


#extent
pdfextent = getrcoldata("Size.")

#unitdate
#inclusive dates
pdfidates = getrcoldata("Inclusive dates.")

#bulk dates
pdfbdates = getrcoldata("Bulk dates.")

#language
pdflanguage = getrcoldata("Language.")
if pdflanguage == "":
    pdflanguage = getrcoldata("Languages.")

#abstract
pdfabstract = getrcoldata("Summary.")

#accessrestrict
pdfaccessrestrict = getrcoldata("Restrictions on access.")
if pdfaccessrestrict == "":
    pdfaccessrestrict = getrcoldata("Access restrictions.")
    
#related material
pdfrelatedmaterial = getrcoldata("Related collections.")
if pdfrelatedmaterial == "":
    pdfrelatedmaterial = getrcoldata("Related collection.")

#copyright
pdfuserestrict = getrcoldata("Copyright.")

#prefercite
pdfprefercite = getrcoldata("Citation.")

#repository - hardcoding the text, should be same for all
pdfcorpname = "Louisiana State University Special Collections"
pdfsubarea = "Louisiana and Lower Mississippi Valley Collection"

#physloc
pdfphysloc = getrcoldata("Stack locations.")
if pdfphysloc == "":
    pdfphysloc = getrcoldata("Stack location.")

#bioghist assuming scope and content always next
pdfbioghist = getalltext("BIOGRAPHICAL/HISTORICAL NOTE","SCOPE AND CONTENT NOTE", "LIST OF SERIES AND SUBSERIES")

#scopecontent - assuming that index terms is always next
pdfscopecontent = getalltext("SCOPE AND CONTENT NOTE", "LIST OF SERIES AND SUBSERIES", "INDEX TERMS")

#arrangement
#series and subseries
almostListSeries = getalltext("LIST OF SERIES AND SUBSERIES", "SERIES DESCRIPTIONS", "INDEX TERMS")
d = "Series"
s =  [d + e for e in almostListSeries.split(d) if e != ""]
#print s
dd = "Subseries"
serieses = []
for a in s:
    l = [g for g in a.split(dd) if g != ""]
    serieses.append(l)
finalseries = []
for i, series in enumerate(serieses):
    finalseries.append("<list><head>" + series[0] + "</head>")
    for ii, m in enumerate(series):
        if ii > 0:
            finalseries.append("<item>Subseries" + series[ii] + "</item>")
    finalseries.append("</list>")
finalseries.insert(0, "<arrangement encodinganalog='351'>")
finalseries.append("</arrangement>")
finalseries = "".join(finalseries)

#series descriptions
seriesdesc = getalltext ("SERIES DESCRIPTIONS", "INDEX TERMS", "CONTAINER LIST")
d = "Series"
print seriesdesc
s = [d + e for e in seriesdesc.split(d) if e != ""]
print type(s)

'''
#using efactory
ead =(
    E.ead(
        E.eadheader(
            E.eadid('', countrycode='us', url=pdfurl),
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
                        E.addressline(pdfaddressline1),
                        E.addressline(pdfaddressline2),
                        E.addressline(pdfaddressline3),
                    ),
                    E.date(pdfdate)
                )
            )
                    
        ),
        E.archdesc(
            E.did(
                E.head(pdfhead),
                E.physdesc('' + '\n\t\t', 
                    E.extent(pdfextent),
                    label='Size', encodinganalog='300$a'
                ),
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
            etree.XML(finalseries)    
            ),
            level='collection', type='inventory', relatedencoding='MARC21'
        )
    )
#)
print etree.tostring(ead, pretty_print=True)
print finalseries + "\n"
print seriesdesc        '''            
