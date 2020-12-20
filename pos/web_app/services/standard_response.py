#!/usr/bin/env python3

# lib imports
import json
import uuid
import datetime
from flask import jsonify

# project imports
from pos.persistance_db_manager.models.customers import Customer
from pos.persistance_db_manager.models.categories import Category
from pos.persistance_db_manager.models.orders import Order
from pos.persistance_db_manager.models.employees import Employee
from pos.persistance_db_manager.models.products import Product
from pos.persistance_db_manager.models.stocks import Stock
from pos.persistance_db_manager.models.suppliers import Supplier
from pos.persistance_db_manager.models.order_items import OrderItem


def default_serializer(obj):
    if isinstance(obj, (Customer, Category, Order, Employee, Product, Stock, Supplier, OrderItem)):
        return obj.to_json()
    elif type(obj) is uuid.UUID:
        return str(obj)
    elif type(obj) is datetime.datetime:
        return obj.strftime("%d-%b-%Y %H:%M:%S")

    raise Exception(f"Can not serialize: {str(type(obj))}")


def serializer(data, indent=4):
    return json.dumps(data, default=default_serializer, indent=indent)


class StandardResponse:

    def __init__(self, data, status):
        self.data = data
        self.status = status

    def to_json(self):
        return serializer({"data": self.data}), self.status

