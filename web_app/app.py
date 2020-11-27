#!/usr/bin/env python3

# lib imports
from flask import Flask

# project imports
from config_manager.config_manager import ConfigManager
from logger_manager.logger_manager import LogManger
from persistance_db_manager.db_driver import DBDriver


app_config = ConfigManager().app_config
logger = LogManger().get_logger(__name__)

db_driver = DBDriver()


def creat_app():

    app = Flask(import_name=__name__)

    logger.info("Flask App created.")

    return app


def start_app(app=None):
    host = app_config.get('FLASK_APP', 'host', fallback='localhost')
    port = app_config.getint('FLASK_APP', 'port', fallback=8008)
    debug = app_config.getboolean('FLASK_APP', 'debug', fallback=False)

    if app is None:
        app = creat_app()

    logger.info(f"App is running on host name: {host}, port: {port}, with debug mode: {debug}")
    app.run(host=host, port=port, debug=debug, use_reloader=False)

