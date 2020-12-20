#!/usr/bin/env python3

# lib imports
from flask import Flask

# project imports
from pos.config_manager.config_manager import ConfigManager
from pos.logger_manager.logger_manager import LogManger
from pos.web_app.api.v1.categories import categories_blueprint
from pos.web_app.api.v1.customers import customers_blueprint
from pos.web_app.api.v1.employees import employees_blueprint
from pos.web_app.api.v1.orders import orders_blueprint
from pos.web_app.api.v1.products import products_blueprint
from pos.web_app.api.v1.stocks import stocks_blueprint
from pos.web_app.api.v1.suppliers import suppliers_blueprint


app_config = ConfigManager().app_config
logger = LogManger().get_logger(__name__)


flask_app = Flask(import_name=__name__)


def creat_app():

    with flask_app.app_context():
        flask_app.config['SECRET_KEY'] = app_config.get('FLASK_APP', 'app_secret')
        flask_app.config['ENV'] = app_config.get('FLASK_APP', 'env')

        # API V1 Registration
        pos_api_v1_base_url = '/spos/api/v1'
        flask_app.register_blueprint(categories_blueprint, url_prefix=pos_api_v1_base_url)
        flask_app.register_blueprint(customers_blueprint, url_prefix=pos_api_v1_base_url)
        flask_app.register_blueprint(employees_blueprint, url_prefix=pos_api_v1_base_url)
        flask_app.register_blueprint(orders_blueprint, url_prefix=pos_api_v1_base_url)
        flask_app.register_blueprint(products_blueprint, url_prefix=pos_api_v1_base_url)
        flask_app.register_blueprint(stocks_blueprint, url_prefix=pos_api_v1_base_url)
        flask_app.register_blueprint(suppliers_blueprint, url_prefix=pos_api_v1_base_url)

        logger.info("Flask App created.")


def start_app():
    host = app_config.get('FLASK_APP', 'host', fallback='localhost')
    port = app_config.getint('FLASK_APP', 'port', fallback=8008)
    debug = app_config.getboolean('FLASK_APP', 'debug', fallback=False)

    creat_app()

    logger.info(f"App is running on host name: {host}, port: {port}, with debug mode: {debug}")
    flask_app.run(host=host, port=port, debug=debug, use_reloader=False)


@flask_app.route('/', methods=['GET'])
def index():
    return {'status': 'SUCCESS'}

