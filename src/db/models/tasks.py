from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from db.db import Base
from db.schemas.tasks import TaskSchema


class Tasks(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[str]
    
    def to_schema(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            author_id=self.author_id,
            title=self.title,
            description=self.description,
            status=self.status
        )