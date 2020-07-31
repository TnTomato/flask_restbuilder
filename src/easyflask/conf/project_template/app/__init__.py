from flask import Flask

from ..extensions.db import sa


def create_app(config_name='debug'):
    app = Flask(__name__)
    sa.init_app(app)
    return app
