#! /usr/bin/env python
# small script to convert text to dict file

subject_term_sets = {
                     'geoname':     {'lcsh': set(),},
                     'persname':    {'lcsh': set(),},
                     'subject':     {'aat':  set(),
                                    'lcsh':  set(),
                                    'local': set(),
                                    },
                     'title_subject': {'lcsh': set(),},
                     'occupation':  {'lcsh': set(),
                                    'local': set(),
                                    },
                     'genreform':   {'aat': set(),
                                    'gmgpc': set(),
                                    'lcsh': set(),
                                    'local': set(),
                                    },
                     'corpname':    {'local': set(),
                                    'lcsh': set(),
                                    },
                    }

for term, source_dict in subject_term_sets.iteritems():
    for source, term_set in source_dict.iteritems():
        with open('field_text_files/{}-{}.txt'.format(term, source)) as f:
            for line in f:
                line = line.strip('\n\r').strip()
                term_set.add(line)

# show items in two sets
dupe_set = []
for term, source_dict in subject_term_sets.iteritems():
    for source, term_set in source_dict.iteritems():
        for uterm, usource_dict in subject_term_sets.iteritems():
            for usource, uterm_set in usource_dict.iteritems():
                if (term, source, term_set) != (uterm, usource, uterm_set):
                    new_union = term_set.intersection(uterm_set)
                    print term, source, '\t', uterm, usource,": ", new_union

#print 'terms_sets_dict = {}'.format(subject_term_sets)
