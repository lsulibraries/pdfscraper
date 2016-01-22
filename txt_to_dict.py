#! /usr/bin/env python
# small script to convert text to dict file

subject_term_sets = {
                     'geoname': set(),
                     'persname': set(),
                     'subject': set(),
                     'title_subject': set(),
                     'occupation': set(),
                     'genreform': set(),
                     'corpname': set(),
                     }

for term, term_set in subject_term_sets.iteritems():
    with open('field_text_files/{}.txt'.format(term)) as f:
        for line in f:
            line = line.strip('\n\r').strip()
            term_set.add(line)

# show items in two sets
# for term, term_set in subject_term_sets.iteritems():
#     for uterm, uterm_set in subject_term_sets.iteritems():
#         if term != uterm:
#             new_union = term_set.intersection(uterm_set)
#             print term, '\t', uterm, ": ", new_union

print 'terms_sets_dict = {}'.format(subject_term_sets)
