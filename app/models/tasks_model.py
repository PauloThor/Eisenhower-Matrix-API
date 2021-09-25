from app.models.categories_model import CategoriesModel
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass, field
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from .eisenhowers_model import EisenhowersModel
from .tasks_categories_model import tasks_categories

from app.configs.database import db

@dataclass
class TasksModel(db.Model):
    id: int
    name: str
    description: str
    duration: int
    eisenhower: EisenhowersModel = field(default_factory=EisenhowersModel)

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String, nullable=False)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey('eisenhowers.id'), nullable=False)