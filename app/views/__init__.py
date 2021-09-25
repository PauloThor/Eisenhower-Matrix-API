from flask import Flask

from .categories_view import bp as bp_category
from .tasks_view import bp as bp_task

def init_app(app: Flask):
    app.register_blueprint(bp_category)
    app.register_blueprint(bp_task)