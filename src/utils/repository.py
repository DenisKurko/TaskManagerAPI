from abc import ABC, abstractmethod
from sqlalchemy import select, insert, delete, update

from db.db import async_session_maker

from utils.exceptions import NotFoundDBError, AlreadyExistError
from sqlalchemy.exc import IntegrityError


class AbstractRepo(ABC):
    @abstractmethod
    async def add(self):
        raise NotImplementedError
        
    @abstractmethod
    async def find_all(self):
        raise NotImplementedError
    
    
        

class SQLAlchemyRepo(AbstractRepo):
    model = None
    
    async def add(self, data: dict): # type: ignore
        async with async_session_maker() as session:
            statement = insert(self.model).values(**data).returning(self.model.id) # type: ignore
            try:
                result = await session.execute(statement)
                await session.commit()
            except IntegrityError:
                raise AlreadyExistError("Object already exist")
            return result.scalar_one()


    async def find_all(self, **filter_by):
        async with async_session_maker() as session:
            conditions = [getattr(self.model, key) == value for key, value in filter_by.items()]
            statement = select(self.model).where(*conditions) # type: ignore
            result_query = await session.execute(statement)
            result_object = result_query.all()
            
            if result_object is None:
                raise NotFoundDBError("Object not found")
            
            return [row[0].to_schema() for row in result_object]
        
    
    async def find(self, **filter_by):
        async with async_session_maker() as session:
            conditions = [getattr(self.model, key) == value for key, value in filter_by.items()]
            statement = select(self.model).where(*conditions).limit(1) # type: ignore
            result_query = await session.execute(statement)
            result_object = result_query.first()
            
            if result_object is None:
                raise NotFoundDBError("Object not found")
            
            return result_object[0].to_schema()
        
        
    async def update(self, id, **data):
        async with async_session_maker() as session:
            statement = update(self.model).where(self.model.id == id).values(**data).returning(self.model) # type: ignore
            result_query = await session.execute(statement)
            result_object = result_query.first()
            
            if result_object is None:
                raise NotFoundDBError("Object not found")
            
            await session.commit()
            return result_object[0].to_schema()
        
    
    async def delete(self, **filter_by):
        async with async_session_maker() as session:
            conditions = [getattr(self.model, key) == value for key, value in filter_by.items()]
            statement = delete(self.model).where(*conditions).returning(self.model.id) # type: ignore
            result = await session.execute(statement)
            await session.commit()
            
            return result.scalar_one()