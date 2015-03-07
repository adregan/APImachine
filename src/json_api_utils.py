''' This is the helper utility for creating responses that follow
    the JSON API (http://jsonapi.org/) spec.
'''

from collections import OrderedDict


class JSONAPI(object):
    def __init__(self, count=0, total_entries=0):
        self.count = count
        self.total_entries = total_entries

    def build_links(self, request_link, page, limit, request_args={}):
        ''' Public method that constructs the links object:
            http://jsonapi.org/format/#document-structure-top-level-links
            mostly containing pagination information:
            http://jsonapi.org/format/#fetching-pagination
        '''
        query_string = '?'
        queries = [
            '{key}={value}'.format(key=key, value=','.join(value))
            for key, value in request_args.items()
        ]
        print (queries)

        links = OrderedDict()
        links['self'] = request_link

        if page > 1:
            links['first'] = ''

        links['last'] = ''
        links['prev'] = ''
        links['next'] = ''

        return links

    def build_meta(self):
        meta = OrderedDict()
        meta['copyright'] = 'Copyright 2015 Andrew Duncan Regan'
        meta['authors'] = ['Duncan Regan']

        return meta
