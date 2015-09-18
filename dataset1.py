#!/usr/bin/env python
# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree, lxml.html
import re
 
# 2. The URL/web address where we can find the PDF we want to scrape
url = 'http://www.lib.lsu.edu/special/findaid/5078.pdf'
 
# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)
 
# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
#print lxml.etree.tostring(root, pretty_print=True)

for page in root:
    assert page.tag == 'page'
    pagelines = { }
    for v in page:
        if v.tag == 'text':
            text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)
            top = int(v.attrib.get('top'))
            if (top - 1) in pagelines:
                top = top - 1
            elif (top + 1) in pagelines:
                top = top + 1
            elif top not in pagelines:
                pagelines[top] = [ ]
            pagelines[top].append((int(v.attrib.get('left')), text))
    lpagelines = pagelines.items()
    lpagelines.sort()
    linepieces = []
    for top, line in lpagelines:
        line.sort()
        pageval = page.attrib.get('number')
        topval = str(top)
        linevalues = []
        for el in line:
            leftval = el[0]
            textval = el[1]
            linevalues = [pageval, topval, leftval, textval]
        if textval == " ":
            continue
        elif textval == "<b> </b>":
            continue
        else:
            linepieces.append(linevalues)
    print linepieces
