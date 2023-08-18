import enum
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

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

    id = Column(Integer, primary_key=True)
    created = db.Column(DateTime, default=db.func.current_timestamp())
    modified = db.Column(DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())


class Task(BaseModel):
    __tablename__ = "task"

    public_id = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(TaskStatus), default=TaskStatus.PROGRESS)
    price_one = Column(Integer, default=0)
    price_two = Column(Integer, default=0)

    def __repr__(self):
        return f"<Task status:{self.status}, assigned to {self.user.username}>"


class User(BaseModel):
    __tablename__ = "user"

    public_id = Column(String(36), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    role = Column(Enum(UserRoles), default=UserRoles.DEVELOPER)
    account = relationship(back_populates="account", uselist=False)

    def __repr__(self):
        return f"<User username:{self.username}, email:{self.email}>"


class Account(BaseModel):
    __tablename__ = "account"

    public_id = Column(String(36), nullable=False, unique=True)
    balance = Column(Integer, default=0)
    user_id = mapped_column(ForeignKey("user.public_id"))
    user = relationship("User", back_populates="account")

    def __repr__(self):
        return f"<Account for {self.user.username}. Balance: {self.balance}>"
