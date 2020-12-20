#!/usr/bin/env python3

# lib imports
from abc import ABCMeta, abstractmethod
from sqlalchemy.ext.declarative import declarative_base


base_model = declarative_base()


class AbstractDBDriver(metaclass=ABCMeta):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def create_employee(self, username, password, name, mobile_phone, address, role):
        pass

    @abstractmethod
    def get_employees(self, username=None, name=None, mobile_phone=None, address=None, role=None, last_modified_by=None):
        pass

    @abstractmethod
    def update_employee(self, username, password=None, name=None, mobile_phone=None, address=None, role=None, last_modified_by=None):
        pass

    @abstractmethod
    def delete_employee(self, username):
        pass

    @abstractmethod
    def create_customer(self, name, mobile_phone, address, last_modified_by):
        pass

    @abstractmethod
    def get_customers(self, name=None, mobile_phone=None, address=None, last_modified_by=None):
        pass

    @abstractmethod
    def update_customer(self, id, last_modified_by, name=None, mobile_phone=None, address=None):
        pass

    @abstractmethod
    def delete_customer(self, id):
        pass

    @abstractmethod
    def create_supplier(self, name, mobile_phone, email, address, last_modified_by):
        pass

    @abstractmethod
    def get_suppliers(self, name=None, mobile_phone=None, email=None, address=None, last_modified_by=None):
        pass

    @abstractmethod
    def update_supplier(self, id, last_modified_by, name=None, email=None, mobile_phone=None, address=None):
        pass

    @abstractmethod
    def delete_supplier(self, id):
        pass

    @abstractmethod
    def create_order(self, order_id, order_date, order_status, order_discount_rate, total_price, customer_id,
                     last_modified_by):
        pass

    @abstractmethod
    def get_orders(self, order_id=None, order_date=None, order_status=None, order_discount_rate=None, total_price=None,
                   customer_id=None, last_modified_by=None):
        pass

    @abstractmethod
    def update_order(self, id, last_modified_by, order_date=None, order_status=None, order_discount_rate=None,
                     total_price=None, customer_id=None):
        pass

    @abstractmethod
    def delete_order(self, id):
        pass

    @abstractmethod
    def create_order_item(self, quantity, price, order_item_discount_rate, product_id, order_id):
        pass

    @abstractmethod
    def get_order_items(self, quantity=None, price=None, order_item_discount_rate=None, product_id=None, order_id=None):
        pass

    @abstractmethod
    def update_order_item(self, id, quantity=None, price=None, order_item_discount_rate=None, product_id=None, order_id=None):
        pass

    @abstractmethod
    def delete_order_item(self, id):
        pass

    @abstractmethod
    def create_category(self, name, description, last_modified_by):
        pass

    @abstractmethod
    def get_categories(self, name=None, description=None, last_modified_by=None):
        pass

    @abstractmethod
    def update_category(self, id, last_modified_by, name=None, description=None):
        pass

    @abstractmethod
    def delete_category(self, id):
        pass

    @abstractmethod
    def create_product(self, name, description, par_code, price, last_modified_by, category_id):
        pass

    @abstractmethod
    def get_products(self, name=None, description=None, par_code=None, price=None, last_modified_by=None, category_id=None):
        pass

    @abstractmethod
    def update_product(self, id, last_modified_by, name=None, description=None, par_code=None, price=None, category_id=None):
        pass

    @abstractmethod
    def delete_product(self, id):
        pass

    @abstractmethod
    def create_stock(self, quantity, retail_price, last_modified_by, supplier_id, product_id):
        pass

    @abstractmethod
    def get_stocks(self, quantity=None, retail_price=None, last_modified_by=None, supplier_id=None, product_id=None):
        pass

    @abstractmethod
    def update_stock(self, id, last_modified_by, quantity=None, retail_price=None, supplier_id=None, product_id=None):
        pass

    @abstractmethod
    def delete_stock(self, id):
        pass
