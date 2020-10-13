# -*- coding: utf-8 -*-
"""
    flask_restbuilder.views
    ~~~~~~~~~~~~~~~~~~~~~~~

    View level helpers.

    :copyright: 2020 TnTomato
    :license: BSD-3-Clause
"""
from flask import request
from flask_restful import Resource, reqparse

from .decorators import exception_handler


class RESTful(Resource):
    """A wrapper of :class:`~flask_restful.Resource`. Easy to build RESTful API
    like ::

        class MyAPI(RESTful):

            def __init__(self):
                if self.method == 'GET':
                    self.parser.add_argument('param', location='args')
                else:
                    self.parser.add_argument('param', location='form')

            def get(self):
                result = self.init_response(data=self.args)
                return result

            def post(self):
                result = self.init_response(data=self.args)
                return result

    Then define routes in routes.py ::

        api.add_resource(MyAPI, '/test', methods=['GET', 'POST'])
    """

    # The request arguments.
    args = None

    # Decide to use exception_handler or not. Reset method_decorators
    # in your API class as you want.
    method_decorators = [exception_handler]

    # An instance of :class:`flask_restful.reqparse.RequestParser` with the
    # default arguments, that makes it an easy parser.
    parser = reqparse.RequestParser()

    @property
    def method(self):
        return request.method

    def add_argument(self, *args, **kwargs):
        """Add arguments to attr:`~flask_restbuilder.RESTful.parser`"""
        self.parser.add_argument(*args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        # Rewrite method:`flask_restful.Resource.dispatch_request` to parse
        # argument from attr:`~flask_restbuilder.RESTful.parser` the default
        # way before handling the request.
        self.args = self.parser.parse_args()
        return super(RESTful, self).dispatch_request(*args, **kwargs)

    @classmethod
    def get_ip(cls) -> str:
        ip = request.headers.get('X-Real-IP') or request.remote_addr
        return ip

    @classmethod
    def init_response(cls, code: int = 200, msg: str = 'ok', data=None) -> dict:
        """Initialize a JSON-like dictionary as a response template"""
        if data is None:
            data = []
        return {'code': code, 'msg': msg, 'data': data}
