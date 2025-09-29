from utils.repository import SQLAlchemyRepo

from db.models.tasks import Tasks


class TasksRepo(SQLAlchemyRepo):
    model = Tasks