#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request

# project imports
from pos.logger_manager.logger_manager import LogManger
from pos.persistance_db_manager.db_driver import DBDriver
from pos.web_app.services.standard_response import StandardResponse

logger = LogManger().get_logger(__name__)

customers_blueprint = Blueprint('customers_blueprint', __name__)


@customers_blueprint.route('/customers', methods=['GET'])
def get_customers():
    try:
        return StandardResponse(DBDriver().get_customers(**request.args), 200).to_json()
    except:
        return StandardResponse('customers do not exist', 404).to_json()


@customers_blueprint.route('/customers', methods=['POST'])
def create_customer():
    json_data = request.json

    customer = (DBDriver().get_customers(mobile_phone=json_data['mobile_phone']) or [None])[0]

    if customer is None:
        try:
            created_customer = DBDriver().create_customer(name=json_data['name'],
                                                          mobile_phone=json_data['mobile_phone'],
                                                          address=json_data.get('address', None),
                                                          last_modified_by=json_data['last_modified_by'])
            return StandardResponse(created_customer, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("category already exists", 406).to_json()


@customers_blueprint.route('/customers/<customer_id>', methods=['PUT', 'PATCH'])
def update_customers(customer_id):
    json_data = request.json

    customer = (DBDriver().get_customers(id=customer_id) or [None])[0]

    if customer is not None:
        try:
            updated_customer = DBDriver().update_customer(id=customer_id,
                                                          name=json_data.get('name', None),
                                                          mobile_phone=json_data.get('mobile_phone', None),
                                                          address=json_data.get('address', None),
                                                          last_modified_by=json_data['last_modified_by'])
            return StandardResponse(updated_customer, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("category does not exist", 406).to_json()


@customers_blueprint.route('/customers/<customer_id>', methods=['DELETE'])
def delete_category(customer_id):

    customer = (DBDriver().get_customers(id=customer_id) or [None])[0]

    if customer is not None:
        try:
            DBDriver().delete_customer(id=customer_id)
            return StandardResponse("customer deleted successfully", 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("customer does not exist", 406).to_json()
