import enum
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class UserRoles(str, enum.Enum):
    ADMIN = 'admin'
    DEVELOPER = 'developer'
    MANAGER = 'manager'


class TaskStatus(str, enum.Enum):
    DONE = 'done'
    PROGRESS = 'in_progress'


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created = db.Column(DateTime, default=db.func.current_timestamp())
    modified = db.Column(DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    role = Column(Enum(UserRoles), default=UserRoles.DEVELOPER)
    tasks = relationship("Task", back_populates='user')

    def __repr__(self):
        return f"<User username:{self.username}, email:{self.email}>"


class Task(BaseModel):
    __tablename__ = "tasks"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")
    description = Column(String(255), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PROGRESS)

    def __repr__(self):
        return f"<Task status:{self.status}, assigned to {self.user.username}>"
