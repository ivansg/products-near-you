# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_cors import CORS
from server.api import api,repo


def create_app(settings_overrides=None):
    app = Flask(__name__)
    configure_settings(app, settings_overrides)
    configure_blueprints(app)
    CORS(app)
    configure_repository(app.config['DATA_PATH'])

    return app


def configure_settings(app, settings_override):
    parent = os.path.dirname(__file__)
    data_path = os.path.join(parent, '..', 'data')
    app.config.update({
        'DEBUG': True,
        'TESTING': False,
        'DATA_PATH': data_path
    })

    if settings_override:
        app.config.update(settings_override)


def configure_blueprints(app):
    app.register_blueprint(api)

def configure_repository(data_path):
    repo.create_repository(data_path)
