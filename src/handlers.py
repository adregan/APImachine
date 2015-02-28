import tornado.web

class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")