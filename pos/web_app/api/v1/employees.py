#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request

# project imports
from pos.logger_manager.logger_manager import LogManger
from pos.persistance_db_manager.db_driver import DBDriver
from pos.web_app.services.standard_response import StandardResponse

logger = LogManger().get_logger(__name__)

employees_blueprint = Blueprint('employees_blueprint', __name__)


@employees_blueprint.route('/employees', methods=['GET'])
def get_employees():
    try:
        return StandardResponse(DBDriver().get_employees(**request.args), 200).to_json()
    except:
        return StandardResponse('employees do not exist', 404).to_json()


@employees_blueprint.route('/employees', methods=['POST'])
def create_employee():
    json_data = request.json

    employee = (DBDriver().get_employees(username=json_data['username']) or [None])[0]

    if employee is None:
        try:
            created_employee = DBDriver().create_employee(username=json_data['username'],
                                                          password=json_data['password'],
                                                          name=json_data['name'],
                                                          mobile_phone=json_data['mobile_phone'],
                                                          address=json_data.get('address', None),
                                                          role=json_data['role'])
            return StandardResponse(created_employee, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("employee already exists", 406).to_json()


@employees_blueprint.route('/employees/<employee_id>', methods=['PUT', 'PATCH'])
def update_employee(employee_id):
    json_data = request.json

    employee = (DBDriver().get_employees(id=employee_id) or [None])[0]

    if employee is not None:
        try:
            updated_employee = DBDriver().update_employee(username=json_data['username'],
                                                          password=json_data.get('password', None),
                                                          name=json_data.get('name', None),
                                                          mobile_phone=json_data.get('mobile_phone', None),
                                                          address=json_data.get('address', None),
                                                          role=json_data.get('role', None))
            return StandardResponse(updated_employee, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("employee does not exist", 406).to_json()


@employees_blueprint.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):

    employee = (DBDriver().get_employees(id=employee_id) or [None])[0]

    if employee is not None:
        try:
            DBDriver().delete_employee(id=employee_id)
            return StandardResponse("employee deleted successfully", 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("employee does not exist", 406).to_json()
