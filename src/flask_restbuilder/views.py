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
    """A wrapper of :class:`flask_restful.Resource`. Easy to build RESTful API
    like ::

        class MyAPI(RESTful):

            def __init__(self):
                super(MyAPI, self).__init__()
                if self.method == 'GET':
                    self.parser.add_argument('param', location='args')
                else:
                    self.parser.add_argument('param', location='form')
                self.parse_arguments()

            def get(self):
                result = self.init_response(data=self.args)
                return result

            def post(self):
                result = self.init_response(data=self.args)
                return result

    Then define routes in routes.py ::

        api.add_resource(MyAPI, '/test', methods=['GET', 'POST'])
    """

    # Decide to use exception_handler or not. Reset method_decorators
    # in your API class as you want.
    method_decorators = [exception_handler]

    def __init__(self):
        # An instance of :class:`flask_restful.reqparse.RequestParser`,
        # makes it easy to use in :class:`~flask_restbuilder.RESTful`
        self.parser = reqparse.RequestParser()

        # Read `args` from `parser` using `self.parse_arguments()`
        self.args = None

    @property
    def method(self):
        return request.method

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

    def parse_arguments(self, req=None, strict=False, http_error_code=400):
        self.args = self.parser.parse_args(req, strict, http_error_code)
