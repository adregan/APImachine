""" Configure your endpoints here.
    The endpoints are a dictionary of routes and handlers which the app will
    use to construct the routes.
"""
from src.handlers import *
from config.schemas import *
from config.models import *

# endpoints = [
#     {"route": "", "handler": DefaultHandler}
# ]

""" This is an example config/testing
"""
endpoints = [
    {"route": r"/?$", "handler": HelloHandler, "name": "hello"},
    {
        "route": r"/tests/?$",
        "handler": DefaultHandler,
        "name": "tests",
        "collection": "tests",
        "schema": TestSchema,
        "methods": ("GET", "OPTIONS", "POST"),
        "model": TestModel
    },
    {
        "route": r"/tests/([\w]+)/?$",
        "handler": DefaultHandler,
        "name": "tests/:id",
        "collection": "tests",
        "schema": TestSchema,
        "methods": ("GET", "OPTIONS", "PATCH", "PUT", "DELETE"),
        "model": TestModel
    }

]