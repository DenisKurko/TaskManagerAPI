from sqlalchemy.orm import mapped_column, Mapped

from db.db import Base
from db.schemas.users import UserSchema


class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    
    def to_schema(self) -> UserSchema:
        return UserSchema(
            user_id=self.id,
            username=self.username,
            password=self.password
        )