from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int
    username: str
    password: str
    
    class Config:
        from_attributes = True
        

class UserGetSchema(BaseModel):
    user_id: int
    username: str
    
    
class UserIDSchema(BaseModel):
    user_id: int
        

class UserCreateSchema(BaseModel):
    username: str
    password: str