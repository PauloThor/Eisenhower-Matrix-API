from sqlalchemy import Column, Integer, String
from dataclasses import dataclass
from app.models.tasks_categories_model import tasks_categories

from app.configs.database import db

@dataclass
class CategoriesModel(db.Model):
    name: str

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String)

    tasks = db.relationship("TasksModel", secondary=tasks_categories, backref="categories", cascade="all, delete")
