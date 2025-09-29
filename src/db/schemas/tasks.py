from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    author_id: int
    title: str
    description: str
    status: str
    
    class Config:
        from_attributes = True
        
        
class TaskIDSchema(BaseModel):
    id: int
        

class TaskPostSchema(BaseModel):
    title: str
    description: str
    status: str

        
class TaskCreateSchema(BaseModel):
    author_id: int
    title: str
    description: str
    status: str