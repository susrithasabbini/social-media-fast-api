from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    ownerId = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    published = Column(Boolean, server_default="TRUE", nullable=False)
    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phoneNumber = Column(String)
    createdAt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vote(Base):
    __tablename__ = "votes"
    userId = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    postId = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
