from flask import Flask

from src.easyflask.conf.project_template.project_name.extensions import sa


def create_app(config_name='debug'):
    app = Flask(__name__)
    sa.init_app(app)
    return app
