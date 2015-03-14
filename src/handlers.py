import tornado.web
import tornado.escape
from src.json_api_utils import JSONAPI
import config.meta as meta
from src.patch_util import Patchy

api = JSONAPI(copyright=meta.copyright, authors=meta.authors)


class DefaultHandler(tornado.web.RequestHandler):

    def initialize(self, collection, schema, methods, model):
        self.collection = collection
        self.schema = schema
        if methods:
            self.SUPPORTED_METHODS = methods
        else:
            self.SUPPORTED_METHODS = ('GET')
        self.model = model

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type')
        self.set_header('Content-Type', 'application/json')

    def write_error(self, err):
        meta = api.build_meta()

        status_code = err.get('status_code', 500)

        default_error = {
            'title': 'Error',
            'detail': 'There was an error',
            'status': status_code
        }
        message = err.get('message', default_error)

        if status_code == 405:
            message = {
                'title': 'Method is not allowed',
                'detail': (
                    'The method {method} is not allowed for {path}'
                    .format(method=self.request.method, path=self.request.uri)
                ),
                'status': 405
            }

        # Set the status code
        self.set_status(status_code)
        # Write the error
        self.write({'errors': message, 'meta': meta})
        # Terminate the request
        self.finish()
        return

    def prepare(self):
        # Grab the full uri and split on args `?`
        path_and_args = self.request.uri.split('?')
        # Keep the path separately
        path = path_and_args.pop(0)
        # Keep the query args in a dictionary if they exist
        args = dict([
            # query_arguments returns byte strings. Decode to utf-8.
            # Also, the value array needs to be split on any commas.
            (key, [value.decode('utf-8') for value in values][0].split(','))
            # We get the arguments from the self.request.query_arguments
            for key, values in self.request.query_arguments.items()
        ])

        # Set a copy of the request link
        self.request_link = '{protocol}://{host}{path}'.format(
            protocol=self.request.protocol,
            host=self.request.host,
            path=path
        )

        self.request_args = args

        return

    def get(self, entry_id=None):
        # Sets an errors list to collect errors
        try:
            # If there is a page declared in the args, pop it into page
            page = self.request_args.pop('page')[0]
        except KeyError:
            # Otherwise, page is 1
            page = 1
        try:
            # If there is a limit, pop the value into limit
            limit = self.request_args['limit'][0]
        except KeyError:
            # Otherwise, limit is 0. Not None, because we try to check
            # the type later and offer feedback and zero works as a truthy
            # when we check against default_request_size
            limit = 0

        # Performs some type checking / coercion on page and limit
        # If there are any problems returns the errors
        try:
            page = int(page)
        except ValueError as error:
            err = api.build_errors(
                title='Query error',
                detail='Incorrect argument type. The page query must be an `integer`.',
                status=400
            )
            self.write_error(err)
            return
        try:
            limit = int(limit)
        except ValueError as error:
            err = api.build_errors(
                title='Query error',
                detail='Incorrect argument type. The limit query must be an `integer`.',
                status=400
            )
            self.write_error(err)
            return

        # If this is a GET request for a single resource
        if entry_id:
            # Check for existing
            existing = self._get_existing(entry_id)
            # If there isn't an existing resource, return a 404
            if not existing:
                err = api.build_errors(
                    title='Resource not found',
                    detail=(
                        'The resource {entry} does not exist for the collection {collection}.'
                        .format(entry=entry_id, collection=self.collection)
                    ),
                    status=404
                )
                self.write_error(err)
                return
            # TODO: Convert existing to whatever the data var will be

        # Sets the request size to either the user defined limit
        # or the default in settings.
        request_size = limit or self.settings.get('default_request_size')

        # TODO: return the total count from database
        # count = len(data)
        # total_entries = total

        # DEV
        count = 10
        total_entries = 55
        # DEV

        # Instantiate the JSON API utility
        if not entry_id:
            api.update_count_total(count=count, total_entries=total_entries)

        links = api.build_links(
            request_link=self.request_link,
            page=page,
            request_size=request_size,
            request_args=self.request_args,
        )
        meta = api.build_meta()

        response = {'links': links, 'data': [], 'meta': meta}

        self.write(response)
        self.set_status(200)
        return

    def post(self):
        # Decode the JSON body
        err, body = self._decode_body()
        # Handle the error, if found
        if err:
            self.write_error(err)
            return
        # Model the data, returns an model object
        modeled = self.model(body)
        # Load the request body into the schema,
        # uses dump to serialize the object to a dictionary
        data, errors = self.schema().dump(modeled)
        # If there were any errors from the schema, return a 400 and the errors
        if errors:
            # TODO: MAKE A REAL ERROR MESSAGE
            self.write_error({'status_code': 400, 'message': errors})
            return

        # Insert the entry into the database
        # TODO: Write the database utility
        # database.insert(self.collection, data)

        # Set the status to 201
        self.write(data)
        self.set_status(201)
        return

    def patch(self, entry_id):
        # TODO: Check for existing entry_id
        existing = self._get_existing(entry_id)
        # If the resource doesn't exist, raise a 404
        if not existing:
            err = api.build_errors(
                title='Resource not found',
                detail=(
                    'The resource {entry} does not exist for the collection {collection}.'
                    .format(entry=entry_id, collection=self.collection)
                ),
                status=404
            )
            self.write_error(err)
            return

        err, body = self._decode_body()
        if err:
            self.write_error(err)
            return

        patchy = Patchy(body)

        err = patchy.validate()

        if err:
            self.write_error(
                api.build_errors(
                    status=400,
                    title='Patch Error',
                    detail=err.get('message')
                )
            )
            return

        self.write({'yo': 'yp'})
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
            self.write_error(err)
            return

        # Model the data, returns an model object
        modeled = self.model(body)
        # Load the request body into the schema,
        # uses dump to serialize the object to a dictionary
        data, errors = self.schema().dump(modeled)
        # If there were any errors from the schema, return a 400 and the errors
        if errors:
            # TODO: MAKE A REAL ERROR MESSAGE
            self.write_error({'status_code': 400, 'message': errors})
            return

        # Update the database with the entry
        # TODO: Write the database utility
        # database.update(self.collection, entry_id, data)

        self.write(data)
        self.set_status(200)
        return

    def delete(self, entry_id):
        # TODO: Check for existing entry_id
        existing = self._get_existing(entry_id)
        # If the resource doesn't exist, raise a 404
        if not existing:
            err = api.build_errors(
                title='Resource not found',
                detail=(
                    'The resource {entry} does not exist for the collection {collection}.'
                    .format(entry=entry_id, collection=self.collection)
                ),
                status=404
            )
            self.write_error(err)
            return

        # Clears the Content-Type header. Only displaying status code
        self.clear_header('Content-Type')
        # Set the status to 204, No Content
        self.set_status(204)
        return

    def options(self):
        # Joins the supported methods to return in the header
        methods = ', '.join(self.SUPPORTED_METHODS)
        # Sets the Access-Control-Allow-Methods header
        self.set_header('Access-Control-Allow-Methods', methods)
        # Clears the Content-Type header as we are only returning headers
        self.clear_header('Content-Type')
        # Set the status to 204, No Content
        self.set_status(204)
        return

    def _get_existing(self, entry_id):
        return True

    def _decode_body(self):
        ''' This method attempts to decode the request's JSON body.
            If it cannot be found or is poorly formatted, returns an error.
        '''
        # Set the variable to None
        err = body = None
        # Check if the request body exists, return 400 if it doesn't
        if not self.request.body:
            err = api.build_errors(
                title='JSON error',
                status=400,
                detail='JSON body is missing. You must include a JSON body.'
            )
        # The request body exists, try to decode it
        else:
            try:
                body = tornado.escape.json_decode(self.request.body)
            # If the request body cannot be decoded, return a 400 error
            except ValueError as error:
                err = api.build_errors(
                    title='JSON error',
                    status=400,
                    detail=(
                        'There is a problem with your JSON formatting: {error}'
                        .format(error=error)
                    )
                )

        # Return the err and/or the decoded body (one will be None)
        return err, body


class HelloHandler(DefaultHandler):
    # TEMPORARY
    # TODO: Put some kind of documentation in at the root route

    def get(self):
        from collections import OrderedDict
        hello = OrderedDict(
            [
                ('greeting', 'Hello there.'),
                ('message', ['How', 'are', 'you', '?'])
            ]
        )
        self.write(hello)
