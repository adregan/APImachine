''' This is the helper utility for creating responses that follow
    the JSON API (http://jsonapi.org/) spec.
'''

from collections import OrderedDict
from math import floor


class JSONAPI(object):
    def __init__(self, count, total_entries):
        self.count = count
        self.total_entries = total_entries

    def build_links(self, request_link, page, request_size, request_args={}):
        ''' Public method that constructs the links object:
            http://jsonapi.org/format/#document-structure-top-level-links
            mostly containing pagination information:
            http://jsonapi.org/format/#fetching-pagination
        '''
        # Builds the query string by breaking down the dictionary
        queries = [
            '{key}={value}'.format(key=key, value=','.join(value))
            for key, value in request_args.items()
        ]
        # Joins queries with ampersands
        query_string = '&'.join(queries)

        # If there is a limit defined, add that to the query string
        # If there is a page defined, add that to the query string
        # Declares a first_page_link and prev_page_link as well
        first_page_link = prev_page_link = None
        if page > 1:
            # Constructs the first_page_link (removes the page query)
            first_page_link = '{link}?{queries}'.format(
                link=request_link,
                queries=query_string
            )
            # Constructs the prev_page_link (subtracts 1 from the page)
            prev_page_link = '{link}?{queries}&page={page}'.format(
                link=request_link,
                queries=query_string,
                page=page-1
            )
            # Sets the query string used by self
            query_string += '&page={page}'.format(page=page)

        last_page_link = next_page_link = None
        if self.total_entries > request_size:
            next_page_link = '{link}?{queries}&page={page}'.format(
                link=request_link,
                queries=query_string,
                page=page+1
            )
            last_page = floor((self.total_entries / request_size) + 1)
            last_page_link = '{link}?{queries}&page={page}'.format(
                link=request_link,
                queries=query_string,
                page=last_page
            )

        # Creates an ordered dict for the links
        links = OrderedDict()
        # If there is a query string, set the self link with it
        if query_string:
            links['self'] = '{link}?{queries}'.format(
                link=request_link,
                queries=query_string
            )
        # Otherwise, self link is the request link
        else:
            links['self'] = request_link

        if first_page_link:
            links['first'] = first_page_link

        if last_page_link:
            links['last'] = last_page_link

        if prev_page_link:
            links['prev'] = prev_page_link

        if next_page_link:
            links['next'] = next_page_link

        return links

    def build_meta(self):
        meta = OrderedDict()
        meta['copyright'] = 'Copyright 2015 Andrew Duncan Regan'
        meta['authors'] = ['Duncan Regan']

        return meta
