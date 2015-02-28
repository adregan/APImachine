import tornado.web
import tornado.escape


class DefaultHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Content-Type", "application/json")

    def get(self):
        self.set_status(200)
        self.write({"message": "Hello"})
        return

    def post(self):
        err, body = self._decode_body()
        if err:
            self._handle_errors(err)
            return

        return

    def patch(self):
        err, body = self._decode_body()
        if err:
            self._handle_errors(err)
            return

        return

    def put(self):
        err, body = self._decode_body()
        if err:
            self._handle_errors(err)
            return

        return

    def delete(self):
        pass

    def options(self):
        pass

    def _decode_body(self):
        err = body = None
        if not self.request.body:
            err = {
                "code": 400,
                "message": "JSON body is missing"
            }
        else:
            try:
                body = tornado.escape.json_decode(self.request.body)
            except ValueError as error:
                err = {
                    "code": 400,
                    "message": (
                        "There is a problem with your JSON formatting: %s"
                        % error
                    )
                }

        return err, body

    def _handle_errors(self, err):
        self.set_status(err.get('code', 500))
        self.write(
            {"error": err.get('message', {})}
        )
        self.finish()
        return
