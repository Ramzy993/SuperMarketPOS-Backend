#!/usr/bin/env python3

# lib imports
from flask import Flask

# project imports


def creat_app():

    app = Flask(import_name=__name__)

    return app


def start_app(app=None):

    if app is None:
        app = creat_app()

    app.run()

