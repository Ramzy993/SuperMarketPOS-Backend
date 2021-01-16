#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request

# project imports
from pos.logger_manager.logger_manager import LogManger
from pos.persistance_db_manager.db_driver import DBDriver
from pos.web_app.services.standard_response import StandardResponse

logger = LogManger().get_logger(__name__)

stocks_blueprint = Blueprint('stocks_blueprint', __name__)


@stocks_blueprint.route('/stocks', methods=['GET'])
def get_stocks():
    try:
        return StandardResponse(DBDriver().get_stocks(**request.args), 200).to_json()
    except:
        return StandardResponse('stocks do not exist', 404).to_json()


@stocks_blueprint.route('/stocks', methods=['POST'])
def create_stock():
    json_data = request.json

    stock = (DBDriver().get_stocks(product_id=json_data['product_id']) or [None])[0]

    if stock is None:
        try:
            created_stock = DBDriver().create_stock(quantity=json_data.get('quantity', None),
                                                    retail_price=json_data.get('retail_price', None),
                                                    last_modified_by=json_data['last_modified_by'],
                                                    supplier_id=json_data.get('supplier_id', None),
                                                    product_id=json_data.get('product_id', None))
            return StandardResponse(created_stock, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("stock already exists", 406).to_json()


@stocks_blueprint.route('/stocks/<stock_id>', methods=['PUT', 'PATCH'])
def update_stocks(stock_id):
    json_data = request.json

    stock = (DBDriver().get_stocks(id=stock_id) or [None])[0]

    if stock is not None:
        try:
            updated_stock = DBDriver().update_stock(id=stock_id, quantity=json_data.get('quantity', None),
                                                    retail_price=json_data.get('retail_price', None),
                                                    last_modified_by=json_data['last_modified_by'],
                                                    supplier_id=json_data.get('supplier_id', None),
                                                    product_id=json_data.get('product_id', None))
            return StandardResponse(updated_stock, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("stock does not exist", 406).to_json()


@stocks_blueprint.route('/stocks/<stock_id>', methods=['DELETE'])
def delete_stock(stock_id):

    stock = (DBDriver().get_stocks(id=stock_id) or [None])[0]

    if stock is not None:
        try:
            DBDriver().delete_stock(id=stock_id)
            return StandardResponse("stock deleted successfully", 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("stock does not exist", 406).to_json()
