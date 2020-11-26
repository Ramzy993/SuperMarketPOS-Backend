#!/usr/bin/env python3

# lib imports
import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship

# project imports
from persistance_db_manager.abstract_db_driver import base_model
from persistance_db_manager.guid import GUID


class OrderItem(base_model):

    __tablename__ = 'order_items'
    __table_args__ = (CheckConstraint('item_discount_rate >= 0 and item_discount_rate < 1',
                                      name='discount_rate_constrain'),)

    id = Column(GUID(), default=uuid.uuid4, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    item_discount_rate = Column(String(128), unique=True, nullable=False)

    product_id = Column(GUID, ForeignKey('products.id'), nullable=False)
    order_id = Column(GUID, ForeignKey('orders.id'), nullable=False)

    order = relationship("Order", uselist=True, backref="order_items")

    def __init__(self, quantity, price, item_discount_rate, product_id, order_id):
        self.quantity = quantity
        self.price = price
        self.item_discount_rate = item_discount_rate
        self.product_id = product_id
        self.order_id = order_id

    def __repr__(self):
        return f"item id: {self.id}. Quantity: {self.quantity}. Price: {self.price}. " \
               f"Item discount rate: {self.item_discount_rate}"

    def to_json(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'price': self.price,
            'item_discount_rate': self.item_discount_rate,
            'product_id': self.product_id,
            'order_id': self.order_id,
        }
