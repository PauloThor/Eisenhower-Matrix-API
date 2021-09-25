from flask import Blueprint, request, current_app, jsonify
from app.models.categories_model import CategoriesModel
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm.exc import UnmappedInstanceError


bp = Blueprint('categories_bp', __name__, url_prefix='/api')

@bp.post('/category')
def create():
    data = request.get_json()

    try:
        category_name = data['name']
        category_description = data['description']

        new_category = CategoriesModel(
        name=category_name,
        description=category_description 
        )

        session = current_app.db.session

        session.add(new_category)
        session.commit()

        return jsonify({
            "id": new_category.id,
            "name": new_category.name,
            "description": new_category.description
        }), 201

    except IntegrityError:
        return {"msg": "category already exists!"}, 409


@bp.patch('/category/<category_id>')
def update(category_id):
    data = request.get_json()

    try:
        updated_category = CategoriesModel.query.get(category_id)

        if 'name' in data:
            updated_category.name = data['name']
        
        if 'description' in data:
            updated_category.description = data['description']

        session = current_app.db.session

        session.add(updated_category)
        session.commit()

        return jsonify(updated_category), 200

    except AttributeError:
        return {"msg": "category not found!"}, 404
    
    except IntegrityError:
        return {"msg": "category already exists!"}, 409



@bp.delete('/category/<category_id>')
def delete(category_id):

    try:
        deleted_category = CategoriesModel.query.get(category_id)

        session = current_app.db.session

        session.delete(deleted_category)
        session.commit()

        return '', 204

    except UnmappedInstanceError:
        return {"msg": "category not found!"}, 404
    
    except IntegrityError:
        return {"msg": "category already exists!"}, 409

             