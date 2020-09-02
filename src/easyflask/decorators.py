# -*- coding: utf-8 -*-
"""
    easyflask.decorators
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: 2020 TnTomato
    :license: BSD-3-Clause
"""
import traceback

from flask import current_app, jsonify, make_response

from .exceptions import BaseError


def exception_handler(func):
    """Catch exceptions and return JSON response"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseError as err:
            return make_response(jsonify(code=err.code, msg=err.message), 200)
        except:
            if current_app.config['DEBUG'] or current_app.config['TESTING']:
                msg = traceback.format_exc()
            else:
                msg = 'Internal Server Error'
            return make_response(jsonify(code=500, msg=msg), 500)
    return wrapper
