""" This is the helper utility for creating responses that follow
    the JSON API (http://jsonapi.org/) spec.
"""

from collections import OrderedDict


class JSONAPI(object):
    def __init__(self, request):
        self.request = request

    def build_links(self):
        """ Public method that constructs the links object:
            http://jsonapi.org/format/#document-structure-top-level-links
            mostly containing pagination information:
            http://jsonapi.org/format/#fetching-pagination
        """

        request_link = "%s://%s%s" % (
            self.request.protocol,
            self.request.host,
            self.request.uri
        )

        links = OrderedDict()

        links["self"] = request_link
        links["first"] = ""
        links["last"] = ""
        links["prev"] = ""
        links["next"] = ""

        return links

    def build_meta(self):
        meta = OrderedDict()
        meta["copyright"] = "Copyright 2015 Andrew Duncan Regan"
        meta["authors"] = ["Duncan Regan"]

        return meta
