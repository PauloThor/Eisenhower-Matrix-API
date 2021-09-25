from app.models.eisenhowers_model import EisenhowersModel
from .tasks_controllers import Task
from app.exc.task_errors import InvalidOptions

class Eisenhower:
    def _init__(self):
        ...
    
    @staticmethod
    def get_eisenhower_type(importance: int, urgency: int):
        eisenhower_sum = importance + urgency

        if eisenhower_sum == 2:
            return 'Do It First'
        
        if eisenhower_sum == 4: 
            return 'Delete It'
        
        return 'Delegate It' if importance == 1 else 'Schedule It'


    @staticmethod
    def get_eisenhower(data): 
        importance = data['importance']
        urgency = data['urgency']
        
        eisenhower_type = Eisenhower.get_eisenhower_type(importance, urgency)
        
        eisenhower = EisenhowersModel.query.filter_by(type = eisenhower_type).one()
        
        return eisenhower

        