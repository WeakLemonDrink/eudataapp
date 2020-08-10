'''
Helper functions for the `profiles` Django app
'''


from tenders.tables import ContractNoticeTable


def get_search_term_matches(search_term_qs, cn_qs):
    '''
    Method loops through any search terms in `search_term_qs` queryet and looks for matches in the
    `cn_qs` ContractNotice queryset Lot search vectors

    If matches are found, a list of dictionaries is returned containing:
      'count' = number of matches for the term
      'table' = a `ContractNoticeTable` containing the queryset of matching `ContractNotice`
                entries
      'term' = the matched search term

    If no matches are found, just returns an empty list
    '''

    search_term_matches = []

    if search_term_qs.exists():
        # Now search for each `TedSearchTerm` in the contract notice qs to see whether we have any
        # matches
        for term in search_term_qs:

            matches_qs = cn_qs.filter(lot__search_vector__icontains=term.keyword).distinct()

            if matches_qs.exists():
                # If matches exist, append the term and a table of data to the list for rendering
                search_term_matches.append(
                    {'count': matches_qs.count(),
                     'table': ContractNoticeTable(matches_qs, orderable=False),
                     'term': term}
                )

    return search_term_matches
