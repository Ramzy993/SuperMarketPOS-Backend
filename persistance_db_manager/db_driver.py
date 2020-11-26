#!/usr/bin/env python3

# lib imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# project imports
from config_manager.config_manager import ConfigManager
from utilities.exception_handler import BaseException
from utilities.patterns.singleton import SingletonDecorator
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


@SingletonDecorator
class DBDriver(AbstractDBDriver):

    def __init__(self):
        super().__init__()
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

        # self.__seed_db()

    def __del__(self):
        self.connection.close()

    def __seed_db(self):
        employee = (self.get_employees(username='ramzy993') or [None])[0]
        if employee is None:
            self.create_employee(username='ramzy993', password='123', name='Youssef Ramzy', mobile_phone='0111',
                                 address='123 st', role='admin')

    def __dynamic_commit(self, model):
        self.session.add(model)
        self.session.commit()
        return model

    def __dynamic_filter(self, model, args_dict):
        if model is None:
            raise DBDriverException("cannot find model")

        args_dict.pop('self')

        query = self.session.query(model)
        model_attr_dict = vars(model)

        for key, value in args_dict.items():
            if value is not None and key in model_attr_dict:
                query = query.filter(getattr(model, key, value))

        return query

    def __dynamic_update(self, model, args_dict):
        if model is None:
            raise DBDriverException("cannot find model")

        args_dict.pop('self')
        args_dict.pop('id', None)

        model_attr_dict = vars(model)

        for key, value in args_dict.items():
            if value is not None and key in model_attr_dict:
                setattr(model, key, value)

        return model

    def create_employee(self, username, password, name, mobile_phone, address, role):
        try:
            employee = Employee(username=username, password=password, name=name,mobile_phone=mobile_phone,
                                role=role, address=address)
            return self.__dynamic_commit(employee)

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def get_employees(self, username=None, name=None, mobile_phone=None, address=None, role=None):
        try:
            employees = self.__dynamic_filter(Employee, locals()).all()
            return employees

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def update_employee(self, username, password=None, name=None, mobile_phone=None, address=None, role=None):
        try:
            employee = self.session.query(Employee).filter_by(username=username).first()
            employee = self.__dynamic_update(Employee, locals())
            self.session.commit()
            return employee

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def delete_employee(self, username):
        try:
            self.session.query(Employee).filter_by(username=username).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def create_customer(self, name, mobile_phone, address, last_modified_by):
        try:
            customer = Customer(name=name, mobile_phone=mobile_phone, address=address, last_modified_by=last_modified_by)
            return self.__dynamic_commit(customer)

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def get_customers(self, name=None, mobile_phone=None, address=None, last_modified_by=None):
        try:
            customers = self.__dynamic_filter(Customer, locals()).all()
            return customers

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def update_customer(self, id, last_modified_by, name=None, mobile_phone=None, address=None):
        try:
            customer = self.session.query(Customer).filter_by(id=id).first()
            customer = self.__dynamic_update(Customer, locals())
            self.session.commit()
            return customer

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def delete_customer(self, id):
        try:
            self.session.query(Customer).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def create_supplier(self, name, mobile_phone, email, address, last_modified_by):
        try:
            supplier = Supplier(name=name,mobile_phone=mobile_phone, email=email, address=address,
                                last_modified_by=last_modified_by)
            return self.__dynamic_commit(supplier)

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def get_suppliers(self, name=None, mobile_phone=None, email=None, address=None, last_modified_by=None):
        try:
            suppliers = self.__dynamic_filter(Supplier, locals()).all()
            return suppliers

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def update_supplier(self, id, last_modified_by, name=None, email=None, mobile_phone=None, address=None):
        try:
            supplier = self.session.query(Supplier).filter_by(id=id).first()
            supplier = self.__dynamic_update(Supplier, locals())
            self.session.commit()
            return supplier

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def delete_supplier(self, id):
        try:
            self.session.query(Supplier).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def create_order(self, order_id, order_date, order_status, order_discount_rate, total_price, customer_id,
                     last_modified_by):
        try:
            order = Order(order_id=order_id, order_date=order_date, order_status=order_status,
                          order_discount_rate=order_discount_rate, last_modified_by=last_modified_by,
                          customer_id=customer_id)
            return self.__dynamic_commit(order)

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def get_orders(self, order_id=None, order_date=None, order_status=None, order_discount_rate=None, total_price=None,
                   customer_id=None, last_modified_by=None):
        try:
            orders = self.__dynamic_filter(Order, locals()).all()
            return orders

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def update_order(self, id, last_modified_by, order_date=None, order_status=None, order_discount_rate=None,
                     total_price=None, customer_id=None):
        try:
            order = self.session.query(Order).filter_by(id=id).first()
            order = self.__dynamic_update(Order, locals())
            self.session.commit()
            return order

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def delete_order(self, id):
        try:
            self.session.query(Order).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def create_order_item(self, quantity, price, order_item_discount_rate, product_id, order_id):
        try:
            order_item = OrderItem(quantity=quantity, price=price, item_discount_rate=order_item_discount_rate,
                                   product_id=product_id, order_id=order_id)
            return self.__dynamic_commit(order_item)

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def get_order_items(self, quantity=None, price=None, order_item_discount_rate=None, product_id=None, order_id=None):
        try:
            order_items = self.__dynamic_filter(OrderItem, locals()).all()
            return order_items

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def update_order_item(self, id, quantity=None, price=None, order_item_discount_rate=None, product_id=None, order_id=None):
        try:
            order_item = self.session.query(OrderItem).filter_by(id=id).first()
            order_item = self.__dynamic_update(OrderItem, locals())
            self.session.commit()
            return order_item

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def delete_order_item(self, id):
        try:
            self.session.query(OrderItem).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def create_category(self, name, description, last_modified_by):
        try:
            category = Category(name=name, description=description, last_modified_by=last_modified_by)
            return self.__dynamic_commit(category)

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def get_categories(self, name=None, description=None, last_modified_by=None):
        try:
            categories = self.__dynamic_filter(Category, locals()).all()
            return categories

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def update_category(self, id, last_modified_by, name=None, description=None):
        try:
            category = self.session.query(Category).filter_by(id=id).first()
            category = self.__dynamic_update(Category, locals())
            self.session.commit()
            return category

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def delete_category(self, id):
        try:
            self.session.query(Category).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def create_product(self, name, description, par_code, price, last_modified_by, category_id):
        try:
            product = Product(name=name, description=description, par_code=par_code, price=price,
                              category_id=category_id, last_modified_by=last_modified_by)
            return self.__dynamic_commit(product)

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def get_products(self, name=None, description=None, par_code=None, price=None, last_modified_by=None, category_id=None):
        try:
            products = self.__dynamic_filter(Product, locals()).all()
            return products

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def update_product(self, id, last_modified_by, name=None, description=None, par_code=None, price=None, category_id=None):
        try:
            product = self.session.query(Product).filter_by(id=id).first()
            product = self.__dynamic_update(Product, locals())
            self.session.commit()
            return product

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def delete_product(self, id):
        try:
            self.session.query(Product).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def create_stock(self, quantity, retail_price, last_modified_by, supplier_id, product_id):
        try:
            stock = Stock(quantity=quantity, retail_price=retail_price, last_modified_by=last_modified_by,
                          product_id=product_id, supplier_id=supplier_id)
            return self.__dynamic_commit(stock)

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def get_stocks(self, quantity=None, retail_price=None, last_modified_by=None, supplier_id=None, product_id=None):
        try:
            stocks = self.__dynamic_filter(Stock, locals()).all()
            return stocks

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def update_stock(self, id, last_modified_by, quantity=None, retail_price=None, supplier_id=None, product_id=None):
        try:
            stock = self.session.query(Stock).filter_by(id=id).first()
            stock = self.__dynamic_update(Stock, locals())
            self.session.commit()
            return stock

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")

    def delete_stock(self, id):
        try:
            self.session.query(Stock).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise DBDriverException(f"Database ERROR: {e}")
