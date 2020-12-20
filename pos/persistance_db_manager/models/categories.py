#!/usr/bin/env python3

# lib imports
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# project imports
from pos.persistance_db_manager.abstract_db_driver import base_model
from pos.persistance_db_manager.guid import GUID


class Category(base_model):

    __tablename__ = 'categories'

    id = Column(GUID(), default=uuid.uuid4, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    last_modified_by = Column(GUID, ForeignKey('employees.id'), nullable=False)
    
    product = relationship("Product", uselist=True, backref="category")

    def __init__(self, name, description, last_modified_by):
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_modified_by = last_modified_by

    def __repr__(self):
        return f"category id: {self.id}. Name: {self.name}. Description: {self.description}"

    def to_json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'last_modified_by': self.last_modified_by,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
