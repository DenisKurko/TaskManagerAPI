from repositories.tasks import TasksRepo
from services.tasks import TasksService

from repositories.users import UsersRepo
from services.users import UsersService

from services.auth import AuthService

from utils.crypt import Crypt


def tasks_service():
    return TasksService(TasksRepo) # type: ignore


def users_service():
    return UsersService(UsersRepo) # type: ignore

def auth_service():
    return AuthService()

def crypt_util():
    return Crypt()