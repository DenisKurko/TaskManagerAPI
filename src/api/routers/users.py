from fastapi import APIRouter, Depends, Request

from db.schemas.users import UserCreateSchema, UserGetSchema, UserIDSchema
from services.users import UsersService

from utils.exceptions import UnauthorizedError

from api.dependencies import users_service

from typing import Annotated


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
async def register(
    user: UserCreateSchema,
    users_service: Annotated[UsersService, Depends(users_service)]
) -> UserIDSchema:
    user_id = await users_service.add(user)
    
    return UserIDSchema(
        user_id=user_id
    )
    
    
@router.get("/me")
async def get_user(
    request: Request,
    users_service: Annotated[UsersService, Depends(users_service)]
) -> UserGetSchema:
    if not request.state.user:
        raise UnauthorizedError("Unauthorized")
    
    user_id = request.state.user.get("user_id")
    
    user = await users_service.find(id = user_id)
    
    return UserGetSchema(
        user_id=user.user_id,
        username=user.username
    )
    


@router.delete("/me")
async def delete_user(
    request: Request,
    users_service: Annotated[UsersService, Depends(users_service)]
) -> UserIDSchema:
    if not request.state.user:
        raise UnauthorizedError("Unauthorized")
    
    user_id = request.state.user.get("user_id")
    
    deleted_user_id = await users_service.delete(user_id)
    
    return UserIDSchema(
        user_id=deleted_user_id
    )