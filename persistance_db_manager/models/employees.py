#!/usr/bin/env python3

# lib imports
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

# project imports
from persistance_db_manager.abstract_db_driver import base_model
from persistance_db_manager.guid import GUID


class Employee(base_model):

    __tablename__ = 'employees'

    id = Column(GUID(), primary_key=True)
    name = Column(String(128), nullable=False)
    mobile_phone = Column(String(128), unique=True, nullable=False)
    address = Column(String(256))
    role = Column(String(128))
    username = Column(String(128))
    password = Column(String(128))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    customer = relationship("Customer", uselist=False, backref="employee")
    supplier = relationship("Supplier", uselist=False, backref="employee")
    Stock = relationship("Stock", uselist=False, backref="employee")
    product = relationship("Product", uselist=False, backref="employee")
    order = relationship("Order", uselist=False, backref="employee")
    category = relationship("Category", uselist=False, backref="employee")

    def __init__(self, name, mobile_phone, address, role, username, password):
        self.name = name
        self.mobile_phone = mobile_phone
        self.address = address
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.role = role
        self.username = username
        self.password = generate_password_hash(password=password)

    def __repr__(self):
        return f"Employee id: {self.id}. Name: {self.name}. Mobile Phone: {self.mobile_phone}. Address: {self.address}." \
               f"Role: {self.role}"

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'mobile_phone': self.mobile_phone,
            'address': self.address,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'role': self.role,
        }
