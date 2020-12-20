#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request

# project imports
from pos.logger_manager.logger_manager import LogManger
from pos.persistance_db_manager.db_driver import DBDriver
from pos.web_app.services.standard_response import StandardResponse

logger = LogManger().get_logger(__name__)

orders_blueprint = Blueprint('orders_blueprint', __name__)


@orders_blueprint.route('/orders', methods=['GET'])
def get_orders():
    try:
        return StandardResponse(DBDriver().get_orders(**request.args), 200).to_json()
    except:
        return StandardResponse('orders do not exist', 404).to_json()


@orders_blueprint.route('/orders', methods=['POST'])
def create_order():
    json_data = request.json

    order = (DBDriver().get_orders(order_id=json_data['order_id']) or [None])[0]
    created_order = DBDriver().create_order(order_id=json_data['order_id'],
                                            order_date=json_data['order_date'],
                                            order_status=json_data['order_status'],
                                            order_discount_rate=json_data['order_discount_rate'],
                                            total_price=json_data['total_price'],
                                            customer_id=json_data['customer_id'],
                                            last_modified_by=json_data['last_modified_by'])
    order_items = []
    for order_item in json_data['order_items']:
        created_order_item = DBDriver().create_order_item(quantity=order_item['quantity'],
                                                          price=order_item['price'],
                                                          order_item_discount_rate=order_item[
                                                              'order_item_discount_rate'],
                                                          product_id=order_item['product_id'],
                                                          order_id=created_order.id)
        order_items.append(created_order_item)
    order = {'order_details': created_order, 'order_items': order_items}
    return StandardResponse(order, 200).to_json()
    if order is None:
        try:
            created_order = DBDriver().create_order(order_id=json_data['order_id'],
                                                    order_date=json_data['order_date'],
                                                    order_status=json_data['order_status'],
                                                    order_discount_rate=json_data['order_discount_rate'],
                                                    total_price=json_data['total_price'],
                                                    customer_id=json_data['customer_id'],
                                                    last_modified_by=json_data['last_modified_by'])
            order_items = []
            for order_item in json_data['order_items']:
                created_order_item = DBDriver().create_order_item(quantity=order_item['quantity'],
                                                                  price=order_item['price'],
                                                                  order_item_discount_rate=order_item['order_item_discount_rate'],
                                                                  product_id=order_item['product_id'],
                                                                  order_id=created_order.id)
                order_items.append(created_order_item)
            order = {'order_details': created_order, 'order_items': order_items}
            return StandardResponse(order, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("order already exists", 406).to_json()


@orders_blueprint.route('/orders/<order_db_id>', methods=['PUT', 'PATCH'])
def update_orders(order_db_id):
    json_data = request.json

    order = (DBDriver().get_orders(id=order_db_id) or [None])[0]

    if order is not None:
        try:
            updated_order = DBDriver().update_order(id=order_db_id,
                                                    last_modified_by=json_data['last_modified_by'],
                                                    order_date=json_data.get('order_date', None),
                                                    order_status=json_data.get('order_status', None),
                                                    order_discount_rate=json_data.get('order_discount_rate', None),
                                                    total_price=json_data.get('total_price', None),
                                                    customer_id=json_data.get('customer_id', None))
            order_items = []
            for order_item in json_data['order_items']:
                updated_order_item = DBDriver().create_order_item(quantity=order_item.get('quantity', None),
                                                                  price=order_item.get('price', None),
                                                                  order_item_discount_rate=order_item.get('order_item_discount_rate', None),
                                                                  product_id=order_item.get('product_id', None),
                                                                  order_id=updated_order.id)
                order_items.append(updated_order_item)
            order = {'order_details': updated_order, 'order_items': order_items}
            return StandardResponse(order, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("order does not exist", 406).to_json()


@orders_blueprint.route('/orders/<order_id>', methods=['DELETE'])
def delete_category(order_id):
    order = (DBDriver().get_orders(order_id=order_id) or [None])[0]

    if order is not None:
        try:
            DBDriver().delete_order(id=order.id)
            return StandardResponse("order deleted successfully", 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("order does not exist", 406).to_json()
