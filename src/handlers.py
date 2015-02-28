import tornado.web
import tornado.escape


class DefaultHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Content-Type", "application/json")

    def get(self, entry_id=None):
        # If this is a GET request for a single resource
        if entry_id:
            # Check for existing 
            existing = self._get_existing(entry_id)
            # If there isn't an existing resource, return a 404
            if not existing:
                err = {
                    "code": 404,
                    "message": "Resource not found."
                }
                self._handle_errors(err)
                return
            # TODO: Convert existing to whatever the data var is

        self.set_status(200)
        self.write({"message": "Hello"})
        return

    def post(self):
        err, body = self._decode_body()
        if err:
            self._handle_errors(err)
            return

        self.set_status(201)
        return

    def patch(self, entry_id):
        # TODO: Check for existing entry_id
        existing = self._get_existing(entry_id)
        # If the resource doesn't exist, raise a 404
        if not existing:
            err = {
                "code": 404,
                "message": "Resource not found."
            }
            self._handle_errors(err)
            return

        err, body = self._decode_body()
        if err:
            self._handle_errors(err)
            return

        self.set_status(200)
        return

    def put(self, entry_id):
        # TODO: Check for existing entry_id
        existing = self._get_existing(entry_id)
        # If the resource doesn't exist, create it using post
        if not existing:
            return self.post()

        err, body = self._decode_body()
        if err:
            self._handle_errors(err)
            return

        self.set_status(200)
        return

    def delete(self):
        # Clears the Content-Type header. Only displaying status code
        self.clear_header("Content-Type")
        # Set the status to 204, No Content
        self.set_status(204)
        return

    def options(self):
        # Joins the supported methods to return in the header
        methods = ', '.join(self.SUPPORTED_METHODS)
        # Sets the Access-Control-Allow-Methods header
        self.set_header('Access-Control-Allow-Methods', methods)
        # Clears the Content-Type header as we are only returning headers
        self.clear_header("Content-Type")
        # Set the status to 204, No Content
        self.set_status(204)
        return

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
