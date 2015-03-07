import tornado.ioloop
from tornado.options import define, options, parse_command_line
from src.application import App
from src.handlers import DefaultHandler
from config.endpoints import endpoints

define('port', default=7777, help='server runs on this port', type=int)
define(
    'default_request_size',
    default=10,
    help='The default request size',
    type=int
)
define('dev', default=False, help='sets the dev toggle', type=bool)


def main():
    parse_command_line()
    app = App(options=options, endpoints=endpoints)
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
