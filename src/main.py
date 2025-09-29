from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from typing import Callable

from api.routers.routers import routers
from utils.exceptions import TaskManagerAPIError
from utils.exceptions import (
    NotFoundDBError,
    AlreadyExistError,
    UnauthorizedError
)

from api.middlewares.auth import auth_middleware

import uvicorn


app = FastAPI(
    version="1.0.0",
    title="Task_Manager_API",
    
)

for router in routers:
    app.include_router(router)
    
    
def create_exception_handler(
    status_code: int, initial_message: str
) -> Callable[[Request, TaskManagerAPIError], JSONResponse]:
    detail = {"message": initial_message}
    
    async def exception_handler(
        _: Request, exc: TaskManagerAPIError
    ) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message
            
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )
        
    return exception_handler # type: ignore


app.add_exception_handler(
    exc_class_or_status_code=NotFoundDBError,
    handler=create_exception_handler(
        status.HTTP_404_NOT_FOUND, "Object does not exist"
    ) # type: ignore
)

app.add_exception_handler(
    exc_class_or_status_code=AlreadyExistError,
    handler=create_exception_handler(
        status.HTTP_409_CONFLICT, "Object already exist"
    ) # type: ignore
)

app.add_exception_handler(
    exc_class_or_status_code=UnauthorizedError,
    handler=create_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "User unauthorized"
    ) #type: ignore
)

app.middleware("http")(auth_middleware)
    
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)