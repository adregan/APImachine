from tornado.web import url, Application
import os

class App(Application):
    def __init__(self, options, endpoints, **overrides):
        self.endpoints = endpoints
        handlers = self._build_handlers()

        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'debug': options.dev,
            "compress_response": True,
        }

        Application.__init__(self, handlers, **settings)


    def _build_handlers(self):
        handlers = [
            url(r"%s?$" % endpoint.get('route'), endpoint.get('handler')) 
            for endpoint in self.endpoints
        ]

        return handlers