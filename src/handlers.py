import tornado.web

class DefaultHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Content-Type", "application/json")

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