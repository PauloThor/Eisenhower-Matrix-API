from flask import Blueprint, request, current_app, jsonify
from app.models.categories_model import CategoriesModel
from app.models.eisenhowers_model import EisenhowersModel
from app.models.tasks_model import TasksModel
from app.controllers.eisenhowers_controller import Eisenhower
from app.controllers.tasks_controllers import Task
from datetime import datetime, timedelta
from app.exc.task_errors import InvalidOptions
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm.exc import UnmappedInstanceError


bp = Blueprint('tasks_bp', __name__, url_prefix='/api')

@bp.post('/task')
def create_task():
    data = request.get_json()

    try:
        Task.verify_keys(data)
        eisenhower = Eisenhower.get_eisenhower(data)

        data['eisenhower_id'] = eisenhower.id
        task_categories = data['categories']
        data.pop('categories')

        new_task = Task.post_task(data, task_categories)     

        session = current_app.db.session

        session.add(new_task)
        session.commit()

        output = Task.format_output(new_task)
        return output, 201

    except InvalidOptions as err:
        return err.msg(data['importance'], data['urgency'])
    
    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {'msg': "task already exists!"}, 409


@bp.patch('/task/<id>')
def update_task(id: int):
    data = request.json

    try:
        if 'eisenhower_id' in data:
            eisenhower = Eisenhower.get_eisenhower(data)
            data['eisenhower_id'] = eisenhower.id
        
        categories = []
        if 'categories' in data:
            categories = data['categories']
            data.pop('categories')

        TasksModel.query.filter_by(id=id).update(data)

        session = current_app.db.session
        session.commit() 

        updated_task = TasksModel.query.get(id)
        
        if len(categories) > 0:
            updated_task = Task.update_categories(updated_task, categories)

        output = Task.format_output(updated_task)

        return jsonify(output)

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {'msg': "a task with that name already exists!"}, 409

    except AttributeError as e:
        print(e)
        return {'msg': "category not found!"}, 404
    
    except InvalidRequestError as e:
        invalid_key = str(e).split(' ')[-1]
        return {'msg': f'invalid key: {invalid_key}'}, 409


@bp.delete('/task/<id>')
def delete_task(id: int):
        try:
            deleted_task = TasksModel.query.get(id)

            session = current_app.db.session

            session.delete(deleted_task)
            session.commit()

            return '', 204
        
        except UnmappedInstanceError:
            return {"msg": "task not found!"}


@bp.get('/')
def get_all():
    categories = CategoriesModel.query.all()

    output = []

    for category in categories:
        tasks = [Task.format_output(TasksModel.query.get(task.id), True) for task in category.tasks]

        output.append({
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "tasks": tasks
        })

    return jsonify(output)