# -*- coding: utf-8 -*-
"""
    easyflask.exceptions
    ~~~~~~~~~~~~~~~~~~~~

    HTTP level exceptions.

    :copyright: 2020 TnTomato
    :license: BSD-3-Clause
"""


class BaseError(Exception):
    """Use as a basic class of Exception in your project:

        from easyflask.exceptions import BaseError

        class MyError(BaseError):
            code = 999
            message = 'My error message'

    Raise errors in your API view everywhere. Each one returns a json response
    about the error.
    """
    code = 0
    message = 'Internal Server Error'

    def __init__(self, *, code: int = None,  message: str = None):
        if message:
            self.message = message
        if code:
            self.code = code


class ParameterError(BaseError):
    code = 10000
    message = 'Invalid paramteter'


class UnauthorizedError(BaseError):
    code = 10001
    message = 'Unauthorized'


class ForbiddenError(BaseError):
    code = 10003
    message = 'Forbidden'


class NotFoundError(BaseError):
    code = 10004
    message = 'Resource not found'
