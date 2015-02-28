import tornado.web

class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")

    def post(self):
        pass

    def patch(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def options(self):
        pass