from sqlalchemy import Column, Integer, String
from dataclasses import dataclass
from sqlalchemy.orm import backref

from app.configs.database import db

@dataclass
class EisenhowersModel(db.Model):
    type: str

    __tablename__ = 'eisenhowers'

    id = Column(Integer, primary_key=True)
    type = Column(String(100))

    tasks = db.relationship("TasksModel", backref="eisenhower", uselist=False)
