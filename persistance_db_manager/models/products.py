#!/usr/bin/env python3

# lib imports
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship

# project imports
from persistance_db_manager.abstract_db_driver import base_model
from persistance_db_manager.guid import GUID


class Product(base_model):

    __tablename__ = 'products'

    id = Column(GUID(), default=uuid.uuid4, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(Text)
    par_code = Column(String(64), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    last_modified_by = Column(GUID, ForeignKey('employees.id'), nullable=False)
    category_id = Column(GUID, ForeignKey('categories.id'), nullable=False)

    Stock = relationship("Stock", uselist=False, backref="product")

    def __init__(self, name, description, par_code, price, last_modified_by, category_id):
        self.name = name
        self.description = description
        self.par_code = par_code
        self.price = price
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_modified_by = last_modified_by
        self.category_id = category_id

    def __repr__(self):
        return f"Product id: {self.id}. Name: {self.name}. Par code: {self.par_code}. Price: {self.price}"

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'par_code': self.par_code,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_modified_by': self.last_modified_by,
            'category_id': self.category_id,
        }
