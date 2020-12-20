#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request

# project imports
from pos.logger_manager.logger_manager import LogManger
from pos.persistance_db_manager.db_driver import DBDriver
from pos.web_app.services.standard_response import StandardResponse

logger = LogManger().get_logger(__name__)

categories_blueprint = Blueprint('categories_blueprint', __name__)


@categories_blueprint.route('/categories', methods=['GET'])
def get_categories():
    try:
        return StandardResponse(DBDriver().get_categories(**request.args), 200).to_json()
    except:
        return StandardResponse('categories do not exist', 404).to_json()


@categories_blueprint.route('/categories', methods=['POST'])
def create_category():
    json_data = request.json

    category = (DBDriver().get_categories(name=json_data['name']) or [None])[0]

    if category is None:
        try:
            created_category = DBDriver().create_category(name=json_data.get('name', None),
                                                          description=json_data.get('description', None),
                                                          last_modified_by=json_data.get('last_modified_by', None))
            return StandardResponse(created_category, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("category already exists", 406).to_json()


@categories_blueprint.route('/categories/<category_id>', methods=['PUT', 'PATCH'])
def update_category(category_id):
    json_data = request.json

    category = (DBDriver().get_categories(id=category_id) or [None])[0]

    if category is not None:
        try:
            updated_category = DBDriver().update_category(id=category_id,
                                                          last_modified_by=json_data.get('last_modified_by'),
                                                          name=json_data.get('name', None),
                                                          description=json_data.get('description', None))
            return StandardResponse(updated_category, 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("category does not exist", 406).to_json()


@categories_blueprint.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):

    category = (DBDriver().get_categories(id=category_id) or [None])[0]

    if category is not None:
        try:
            DBDriver().delete_category(id=category_id)
            return StandardResponse("category deleted successfully", 200).to_json()
        except:
            return StandardResponse("check request json format", 400).to_json()
    else:
        return StandardResponse("category does not exist", 406).to_json()
