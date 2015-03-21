import tornado.ioloop
from tornado.options import define, options, parse_config_file, parse_command_line
from tornado.options import Error as ParseError
from src.application import App
from src.handlers import DefaultHandler
from config.endpoints import endpoints
import logging

define('port', default=7777, help='server runs on this port', type=int)
define('dev', default=False, help='sets the dev toggle', type=bool)
define('conf', default='/etc/apimachine.conf', help='The conf file', type=str)
define('database_name', default=None, help='The database name', type=str)
define('database_user', default=None, help='The database user', type=str)
define('database_password', default=None, help='The database password', type=str)
define('database_host', default=None, help='The database host', type=str)
define('database_port', default=None, help='The database port', type=int)
define('default_request_size', default=10, help='The default request size', type=int)


def main():
    try:
        parse_config_file(options.conf)
    except FileNotFoundError as error:
        logging.error(
            'Conf file not found. Location: {conf}'
            .format(conf=options.conf)
        )
        exit(1)
    except SyntaxError as error:
        logging.error(
            'There is an error with your conf syntax: {error}'
            .format(error=error)
        )
        exit(1)
    except ParseError as error:
        logging.error(
            'Incorrect types in you conf file: {error}'
            .format(error=error)
        )
        exit(1)

    parse_command_line()
    app = App(options=options, endpoints=endpoints)
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
