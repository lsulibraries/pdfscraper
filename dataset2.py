#!/usr/bin/env python

# 1. Add some necessary libraries
import scraperwiki, urllib2
from lxml import etree
from lxml.builder import E
 
# 2. The URL/web address where we can find the PDF we want to scrape
pdfurl = 'http://www.lib.lsu.edu/special/findaid/5078.pdf' #Bankston
#pdfurl = 'http://www.lib.lsu.edu/systems/images/0000418.pdf' #Acy papers
#pdfurl = 'http://lib.lsu.edu/special/findaid/0826.pdf' #Guion Diary
#pdfurl = 'http://lib.lsu.edu/special/findaid/4452.pdf' #Turnbull - multiple page biographical note
 
# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(pdfurl).read()
xmldata = scraperwiki.pdftoxml(pdfdata)

#print type(pdfdata)
root = etree.fromstring(xmldata)
 
# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
#print etree.tostring(root, pretty_print=True)
