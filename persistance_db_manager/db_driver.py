#!/usr/bin/env python3

# lib imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# project imports
from config_manager.config_manager import ConfigManager
from utilities.exception_handler import BaseException
from utilities.patterns.singleton import Singleton
from persistance_db_manager.abstract_db_driver import AbstractDBDriver, base_model
from persistance_db_manager.models.customers import Customer
from persistance_db_manager.models.categories import Category
from persistance_db_manager.models.orders import Order
from persistance_db_manager.models.employees import Employee
from persistance_db_manager.models.products import Product
from persistance_db_manager.models.stocks import Stock
from persistance_db_manager.models.suppliers import Supplier
from persistance_db_manager.models.order_items import OrderItem


app_config = ConfigManager().app_config


class DBDriverException(BaseException):
    pass


class DBDriver(AbstractDBDriver, Singleton):

    def __init__(self):
        pass

    def init(self, *args, **kwargs):
        self.dialect = app_config.get('DATABASE', 'dialect', fallback='sqlite')
        self.database_name = app_config.get('DATABASE', 'database_name')
        self.host = app_config.get('DATABASE', 'host')
        self.username = app_config.get('DATABASE', 'username')
        self.password = app_config.get('DATABASE', 'password')

        if self.dialect == 'sqlite':
            self.connection_string = self.dialect + ":///tmp/" + self.database_name + '.db'
        else:
            self.connection_string = self.dialect + "://" + self.username + ":" + self.password + "@" + \
                                     self.host + "/" + self.database_name

        self.engine = create_engine(self.connection_string)

        base_model.metadata.create_all(self.engine)

        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)()

    def __del__(self):
        self.connection.close()
