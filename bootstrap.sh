#! /bin/bash

sudo apt-get update
sudo apt-get install -y libxml2-dev libxslt-dev python-dev python-pip python-lxml zlib1g-dev pdftohtml
sudo pip install --upgrade lxml scraperwiki
