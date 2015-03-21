''' This is the helper utility for creating responses that follow
    the JSON API (http://jsonapi.org/) spec.
'''

from collections import OrderedDict
from math import floor


class JSONAPI(object):

    def __init__(self, copyright=None, authors=None):
        self.copyright = copyright
        self.authors = authors
        self.count = 0
        self.total_entries = 0

    def update_count_total(self, count, total_entries):
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
        self_link = first_page_link = prev_page_link = None

        # Constructs these links when the page is greater than 1
        if page > 1:
            # If there is a query string, attach it to the links, append page
            if query_string:
                # The current page
                self_link = '{link}?{queries}&page={page}'.format(
                    link=request_link,
                    queries=query_string,
                    page=page
                )
                # Constructs the first_page_link (removes the page query)
                first_page_link = '{link}?{queries}'.format(
                    link=request_link,
                    queries=query_string
                )
                # Constructs the prev_page_link (subtracts 1 from the page)
                prev_page_link = '{link}?{queries}&page={page}'.format(
                    link=request_link,
                    queries=query_string,
                    page=page - 1
                )
            # Otherwise, just attach append the page query
            else:
                self_link = '{link}?page={page}'.format(
                    link=request_link,
                    page=page
                )
                # First page is simply the request link
                first_page_link = request_link
                # Constructs the prev_page_link (subtracts 1 from the page)
                prev_page_link = '{link}?page={page}'.format(
                    link=request_link,
                    page=page - 1
                )

        # Works on constructing the last page and the next page
        last_page_link = next_page_link = None
        if self.total_entries > request_size:
            last_page = floor((self.total_entries / request_size) + 1)
            # Restricts last and next when you are on the last page
            if page != last_page and not (page > last_page):
                # If there is a query string, attach it to the links
                # and append the page
                if query_string:
                    last_page_link = '{link}?{queries}&page={page}'.format(
                        link=request_link,
                        queries=query_string,
                        page=last_page
                    )
                    # Next is this page + 1
                    next_page_link = '{link}?{queries}&page={page}'.format(
                        link=request_link,
                        queries=query_string,
                        page=page + 1
                    )
                else:
                    last_page_link = '{link}?page={page}'.format(
                        link=request_link,
                        page=last_page
                    )
                    # Next is this page + 1
                    next_page_link = '{link}?page={page}'.format(
                        link=request_link,
                        page=page + 1
                    )

        # Creates an ordered dict for the links
        links = OrderedDict()
        # If there is a query string, set the self link with it
        if self_link:
            links['self'] = self_link
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
        if self.count:
            meta['count'] = self.count
        if self.total_entries:
            meta['total'] = self.total_entries
        if self.copyright:
            meta['copyright'] = self.copyright
        if self.authors:
            meta['authors'] = self.authors

        return meta

    def build_errors(
        self,
        status,
        title,
        detail,
        err_id=None,
        href=None,
        code=None,
        links=None,
        paths=None
    ):
        # Ensure that status is an int
        try:
            status = int(status)
        # Any problems should return a 500 as this is a problem.
        except (TypeError, ValueError):
            status = 500

        error = {}
        error['title'] = title
        error['status'] = str(status)
        error['detail'] = detail
        if code:
            error['code'] = code
        if paths:
            error['paths'] = paths
        if links:
            error['links'] = links
        if href:
            error['href'] = href
        if err_id:
            error['err_id'] = err_id

        return {'status_code': status, 'message': error}

    def clean(self):
        self.count = self.total_entries = 0
