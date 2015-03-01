import tornado.web
import tornado.escape


class DefaultHandler(tornado.web.RequestHandler):

    def initialize(self, collection, schema, methods, model):
        self.collection = collection
        self.schema = schema()
        self.SUPPORTED_METHODS = methods
        self.model = model

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):
        message = kwargs.get('message', 'There was an error')

        if status_code == 405:
            message = (
                "The method %s is not allowed for %s"
                % (self.request.method, self.request.uri)
            )
        elif status_code == 404:
            message = "Resource not found."

        # Set the status code
        self.set_status(status_code)
        # Write the error
        self.write({"errors": message})
        # Terminate the request
        self.finish()
        return

    def get(self, entry_id=None):
        # If this is a GET request for a single resource
        if entry_id:
            # Check for existing
            existing = self._get_existing(entry_id)
            # If there isn't an existing resource, return a 404
            if not existing:
                self.write_error(404, message="Resource not found.")
                return
            # TODO: Convert existing to whatever the data var is

        self.set_status(200)
        return

    def post(self):
        # Decode the JSON body
        err, body = self._decode_body()
        # Handle the error, if found
        if err:
            self.write_error(err.get('code'), message=err.get('message'))
            return
        # Model the data, returns an model object
        modeled = self.model(body)
        # Load the request body into the schema,
        # uses dump to serialize the object to a dictionary
        data, errors = self.schema.dump(modeled)
        # If there were any errors from the schema, return a 400 and the errors
        if errors:
            self.write_error(400, message=errors)
            return

        # Insert the entry into the database
        # TODO: Write the database utility
        database.insert(self.collection, data)

        # Set the status to 201
        self.write(data)
        self.set_status(201)
        return

    def patch(self, entry_id):
        # TODO: Check for existing entry_id
        existing = self._get_existing(entry_id)
        # If the resource doesn't exist, raise a 404
        if not existing:
            self.write_error(404)
            return

        err, body = self._decode_body()
        if err:
            self.write_error(err.get('code'), message=err.get('message'))
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
            self.write_error(err.get('code'), message=err.get('message'))
            return

        # Model the data, returns an model object
        modeled = self.model(body)
        # Load the request body into the schema,
        # uses dump to serialize the object to a dictionary
        data, errors = self.schema.dump(modeled)
        # If there were any errors from the schema, return a 400 and the errors
        if errors:
            self.write_error(404, message=errors)
            return

        # Update the database with the entry
        # TODO: Write the database utility
        database.update(self.collection, entry_id, data)

        self.write(data)
        self.set_status(200)
        return

    def delete(self, entry_id):
        # TODO: Check for existing entry_id
        existing = self._get_existing(entry_id)
        # If the resource doesn't exist, raise a 404
        if not existing:
            self.write_error(404)
            return

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

    def _get_existing(self, entry_id):
        return True

    def _decode_body(self):
        """ This method attempts to decode the request's JSON body.
            If it cannot be found or is poorly formatted, returns an error.
        """
        # Set the variable to None
        err = body = None
        # Check if the request body exists, return 400 if it doesn't
        if not self.request.body:
            err = {
                "code": 400,
                "message": "JSON body is missing"
            }
        # The request body exists, try to decode it
        else:
            try:
                body = tornado.escape.json_decode(self.request.body)
            # If the request body cannot be decoded, return a 400 error
            except ValueError as error:
                err = {
                    "code": 400,
                    "message": (
                        "There is a problem with your JSON formatting: %s"
                        % error
                    )
                }
        # Return the err and/or the decoded body (one will be None)
        return err, body


class HelloHandler(DefaultHandler):
    # TEMPORARY
    # TODO: Put some kind of documentation in at the root route

    def get(self):
        from collections import OrderedDict
        hello = OrderedDict(
            [
                ("greeting", "Hello there."),
                ("message", ["How", "are", "you", "?"])
            ]
        )
        self.write(hello)
