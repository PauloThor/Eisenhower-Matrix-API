from app.models.tasks_model import TasksModel
from app.exc.task_errors import InvalidOptions
from app.models.categories_model import CategoriesModel
from flask import current_app

class Task:
    def _init__(self):
        ...
    
    @staticmethod
    def format_output(task: TasksModel, shouldRemoveCategories = False):
        output = {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'duration': task.duration,
            'eisenhower_classification': task.eisenhower.type,
            'category': task.categories
        }

        if shouldRemoveCategories:
            priority = output['eisenhower_classification']
            output.pop('category')
            output.pop('eisenhower_classification')
            output.pop('duration')
            output['priority'] = priority

        return output
        
    
    @staticmethod
    def verify_keys(data):
        importance = data['importance']
        urgency = data['urgency']

        if importance > 2 or urgency > 2:
            raise InvalidOptions(importance, urgency)


    @staticmethod
    def post_task(data, categories):
        new_task = TasksModel(**data)

        for category in categories:
            found_category = CategoriesModel.query.filter_by(name=category['name']).first()
            new_task.categories.append(found_category) 

        return new_task

    
    @staticmethod
    def update_categories(updated_task, categories): 
            updated_task.categories = []
            for category in categories:
                found_category = CategoriesModel.query.filter_by(name=category['name']).first()
                updated_task.categories.append(found_category)

            session = current_app.db.session
            session.add(updated_task)
            session.commit() 

            return updated_task
