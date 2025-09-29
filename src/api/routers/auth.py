from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm

from services.users import UsersService
from services.auth import AuthService

from db.schemas.auth import TokenSchema

from utils.crypt import Crypt
from utils.exceptions import NotFoundDBError

from api.dependencies import users_service, auth_service, crypt_util

from typing import Annotated


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    users_service: Annotated[UsersService, Depends(users_service)],
    auth_service: Annotated[AuthService, Depends(auth_service)],
    crypt_util: Annotated[Crypt, Depends(crypt_util)],
    response: Response
):
    user_dict = await users_service.find(username = form_data.username)
    
    if not user_dict or not await crypt_util.verify_password(form_data.password, user_dict.password):
        raise NotFoundDBError(message="Invalid credentials")
    
    access_token = auth_service.create_access_token(
            data={
                "sub": str(user_dict.user_id),
                "username": str(user_dict.username)
            }
    )
    
    response.set_cookie(key="auth", value=access_token)
    return TokenSchema(access_token=access_token,token_type="bearer")