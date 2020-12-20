#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request

# project imports
from pos.logger_manager.logger_manager import LogManger
from pos.persistance_db_manager.db_driver import DBDriver
from pos.web_app.services.standard_response import StandardResponse

logger = LogManger().get_logger(__name__)


products_blueprint = Blueprint('products_blueprint', __name__)


@products_blueprint.route('/products', methods=['GET'])
def get_products():
    try:
        return StandardResponse(DBDriver().get_products(**request.args), 200).to_json()
    except:
        return StandardResponse('products do not exist', 404).to_json()


@products_blueprint.route('/products', methods=['POST'])
def create_product():
    json_data = request.json

    product = (DBDriver().get_products(name=json_data['name']) or [None])[0]

    if product is None:
        try:
            created_product = DBDriver().create_product(name=json_data['name'],
                                                        description=json_data.get('description', None),
                                                        par_code=json_data['par_code'],
                                                        price=json_data['price'],
                                                        last_modified_by=json_data['last_modified_by'],
                                                        category_id=json_data['category_id'])
            return StandardResponse(created_product, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("product already exists", 406).to_json()


@products_blueprint.route('/products/<product_id>', methods=['PUT', 'PATCH'])
def update_products(product_id):
    json_data = request.json

    product = (DBDriver().get_products(id=product_id) or [None])[0]

    if product is not None:
        try:
            updated_product = DBDriver().update_product(id=product_id,
                                                        last_modified_by=json_data['last_modified_by'],
                                                        name=json_data.get('name', None),
                                                        description=json_data.get('description', None),
                                                        par_code=json_data.get('par_code', None),
                                                        price=json_data.get('price', None),
                                                        category_id=json_data.get('category_id', None))
            return StandardResponse(updated_product, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("product does not exist", 406).to_json()


@products_blueprint.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):

    product = (DBDriver().get_products(id=product_id) or [None])[0]

    if product is not None:
        try:
            DBDriver().delete_product(id=product_id)
            return StandardResponse("product deleted successfully", 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("product does not exist", 406).to_json()
