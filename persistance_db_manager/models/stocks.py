#!/usr/bin/env python3

# lib imports
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer

# project imports
from persistance_db_manager.abstract_db_driver import base_model
from persistance_db_manager.guid import GUID


class Stock(base_model):

    __tablename__ = 'stocks'

    id = Column(GUID(), default=uuid.uuid4, primary_key=True)
    quantity = Column(Integer, nullable=False)
    retail_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    last_modified_by = Column(GUID, ForeignKey('employees.id'), nullable=False)
    product_id = Column(GUID, ForeignKey('products.id'), nullable=False)
    supplier_id = Column(GUID, ForeignKey('suppliers.id'), nullable=False)

    def __init__(self, quantity, retail_price, last_modified_by, product_id, supplier_id):
        self.quantity = quantity
        self.retail_price = retail_price
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_modified_by = last_modified_by
        self.product_id = product_id
        self.supplier_id = supplier_id

    def __repr__(self):
        return f"Stock id: {self.id}. Quantity: {self.quantity}. Retail price: {self.retail_price}"

    def to_json(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'retail_price': self.retail_price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_modified_by': self.last_modified_by,
            'product_id': self.product_id,
            'supplier_id': self.supplier_id,
        }
