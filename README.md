# pdfscraper
To convert LSU's legacy pdf finding aids into EAD documents.

The script relies on a python library called scraperwiki. It converts the pdf into xml. Page number is one level of it, with the location on the page indicated by attributes: top, left, width, etc.

This document has a brief explanation of what scraperwiki is doing, starting at page 14. http://davidhuynh.net/spaces/nicar2011/tutorial.pdf But rather than put the data into a dictionary, I opted for converting it directly into the target XML, EAD.
