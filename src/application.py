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
        handlers = [self._build_url(endpoint) for endpoint in self.endpoints]

        return handlers

    def _build_url(self, endpoint):
        route = endpoint.get('route')
        handler = endpoint.get('handler')
        name = endpoint.get('name')
        kwargs = {
            "collection": endpoint.get('collection'),
            "schema": endpoint.get('schema'),
            "methods": endpoint.get('methods'),
            "model": endpoint.get('model')
        }
        route_url = url(route, handler, kwargs, name=name)

        return route_url