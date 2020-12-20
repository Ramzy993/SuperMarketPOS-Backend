#!/usr/bin/env python3

# lib imports
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# project imports
from pos.persistance_db_manager.abstract_db_driver import base_model
from pos.persistance_db_manager.guid import GUID


class Customer(base_model):

    __tablename__ = 'customers'

    id = Column(GUID(), default=uuid.uuid4, primary_key=True)
    name = Column(String(128), nullable=False)
    mobile_phone = Column(String(128), unique=True, nullable=False)
    address = Column(String(256))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    last_modified_by = Column(GUID, ForeignKey('employees.id'), nullable=False)

    order = relationship("Order", uselist=True, backref="customer")

    def __init__(self, name, mobile_phone, address, last_modified_by):
        self.name = name
        self.mobile_phone = mobile_phone
        self.address = address
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_modified_by = last_modified_by

    def __repr__(self):
        return f"customer id: {self.id}. Name: {self.name}. Mobile Phone: {self.mobile_phone}. Address: {self.address}"

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'mobile_phone': self.mobile_phone,
            'address': self.address,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_modified_by': self.last_modified_by,
        }
