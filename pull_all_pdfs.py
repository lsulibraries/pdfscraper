#! /usr/bin/env python3

import os
import urllib2

# our_list = 'findaid_list.csv'
# our_list = 'temporarily_unavailalble.csv'
our_list = 'problem_pdf.csv'


def pull_pdf_and_write_to_disk(uid):
    if 'cached_pdfs' not in os.listdir(os.getcwd()):
        os.mkdir('cached_pdfs')
    url = 'http://lib.lsu.edu/sites/default/files/sc/findaid/{}.pdf'.format(uid)
    response = urllib2.urlopen(url).read()
    filename = '{}/cached_pdfs/{}.pdf'.format(os.getcwd(), uid)
    with open(filename, 'w') as f:
        f.write(response)

with open(our_list, 'r') as file:
    for uid in file.readlines():
        uid = uid.strip()
        print(uid)
        if '{}.pdf'.format(uid) in '{}/cached_pdfs'.format(os.getcwd()):
            print('item there')
            pass
        else:
            try:
                pull_pdf_and_write_to_disk(uid)
            except urllib2.HTTPError:
                print('pdf not available at url')
