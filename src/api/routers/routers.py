from api.routers.tasks import router as tasks_router
from api.routers.users import router as users_router
from api.routers.auth import router as auth_router


routers = [
    tasks_router,
    users_router,
    auth_router 
]