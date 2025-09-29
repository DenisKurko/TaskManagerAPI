from utils.repository import SQLAlchemyRepo

from db.models.users import Users


class UsersRepo(SQLAlchemyRepo):
    model = Users