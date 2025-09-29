from db.schemas.users import UserCreateSchema, UserSchema
from utils.repository import AbstractRepo
from utils.crypt import Crypt

from typing import Annotated


class UsersService:
    def __init__(self, users_repo: AbstractRepo) -> None:
        self.users_repo = users_repo() # type: ignore
        
    
    async def add(self, user: UserCreateSchema, crypt_context: Crypt = Crypt()):
        hashed_password = await crypt_context.get_password_hash(user.password)
        
        db_user = UserCreateSchema(
            username=user.username,
            password=hashed_password
        )
        
        user_dict = db_user.model_dump()
        
        user_id = await self.users_repo.add(user_dict)
        
        return user_id
    
    
    async def find(self, **filter_by) -> UserSchema:
        user = await self.users_repo.find(**filter_by)
        
        return user
    
    
    async def delete(self, user_id: int):
        user_id = await self.users_repo.delete(id = user_id)

        return user_id