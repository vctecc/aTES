import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created = db.Column(DateTime, default=db.func.current_timestamp())
    modified = db.Column(DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())


class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String(255))
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"

    def __str__(self):
        return self.name


class User(BaseModel):

    __tablename__ = "users"

    public_id = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255))

    role_id = Column(String(36), ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<User username:{self.username}, email:{self.email}>"
