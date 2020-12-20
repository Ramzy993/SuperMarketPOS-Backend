#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request

# project imports
from pos.logger_manager.logger_manager import LogManger
from pos.persistance_db_manager.db_driver import DBDriver
from pos.web_app.services.standard_response import StandardResponse

logger = LogManger().get_logger(__name__)

suppliers_blueprint = Blueprint('suppliers_blueprint', __name__)


@suppliers_blueprint.route('/suppliers', methods=['GET'])
def get_suppliers():
    try:
        return StandardResponse(DBDriver().get_suppliers(**request.args), 200).to_json()
    except:
        return StandardResponse('suppliers do not exist', 404).to_json()


@suppliers_blueprint.route('/suppliers', methods=['POST'])
def create_supplier():
    json_data = request.json

    supplier = (DBDriver().get_suppliers(mobile_phone=json_data['mobile_phone']) or [None])[0]

    if supplier is None:
        try:
            created_supplier = DBDriver().create_supplier(name=json_data['name'],
                                                          mobile_phone=json_data['mobile_phone'],
                                                          address=json_data.get('address', None),
                                                          email=json_data.get('email', None),
                                                          last_modified_by=json_data['last_modified_by'])
            return StandardResponse(created_supplier, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("category already exists", 406).to_json()


@suppliers_blueprint.route('/suppliers/<supplier_id>', methods=['PUT', 'PATCH'])
def update_suppliers(supplier_id):
    json_data = request.json

    supplier = (DBDriver().get_suppliers(id=supplier_id) or [None])[0]

    if supplier is not None:
        try:
            updated_supplier = DBDriver().update_supplier(id=supplier_id, name=json_data['name'],
                                                          mobile_phone=json_data['mobile_phone'],
                                                          address=json_data['address'], email=json_data['email'],
                                                          last_modified_by=json_data['last_modified_by'])
            return StandardResponse(updated_supplier, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("category does not exist", 406).to_json()


@suppliers_blueprint.route('/suppliers/<supplier_id>', methods=['DELETE'])
def delete_category(supplier_id):
    supplier = (DBDriver().get_suppliers(id=supplier_id) or [None])[0]

    if supplier is not None:
        try:
            DBDriver().delete_supplier(id=supplier_id)
            return StandardResponse("supplier deleted successfully", 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("category does not exist", 406).to_json()
