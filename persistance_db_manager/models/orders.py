#!/usr/bin/env python3

# lib imports
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship

# project imports
from persistance_db_manager.abstract_db_driver import base_model
from persistance_db_manager.guid import GUID


class Order(base_model):

    __tablename__ = 'orders'
    __table_args__ = (CheckConstraint('order_discount_rate >= 0 and order_discount_rate < 1',
                                      name='discount_rate_constrain'),)

    id = Column(GUID(), primary_key=True)
    order_id = Column(Integer, unique=True, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_status = Column(String(128), nullable=False)
    order_discount_rate = Column(String(128), unique=True, nullable=False)
    total_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    last_modified_by = Column(GUID, ForeignKey('employees.id'), nullable=False)
    customer_id = Column(GUID, ForeignKey('customers.id'), nullable=False)

    customer = relationship("Customer", uselist=True, backref="orders")

    def __init__(self, order_id, order_date, order_status, order_discount_rate, last_modified_by, customer_id):
        self.order_id = order_id
        self.order_date = order_date
        self.order_status = order_status
        self.order_discount_rate = order_discount_rate
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_modified_by = last_modified_by
        self.customer_id = customer_id

    def __repr__(self):
        return f"Order table id: {self.id}. Order id: {self.order_id}. Order date: {self.order_date}. Order Status: " \
               f"{self.order_status}. Order discount rate: {self.order_discount_rate}"

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'order_date': self.order_date,
            'order_status': self.order_status,
            'order_discount_rate': self.order_discount_rate,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_modified_by': self.last_modified_by,
            'customer_id': self.customer_id,
        }
