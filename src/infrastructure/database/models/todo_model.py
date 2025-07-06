from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.infrastructure.database.connection import Base
import uuid


class TodoModel(Base):
    __tablename__ = "todos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)