from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base

# class Base(DeclarativeBase):
#     pass


class Post(Base):
    __tablename__ = "posts"

    class Config:
        from_attributes = True

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        server_default=text("gen_random_uuid()")
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id: Mapped[str] = mapped_column(
        String, 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    owner = relationship("User")

    class Config:
        from_attributes = True


class User(Base):
    __tablename__ = "users"
    
    class Config:
        from_attributes = True

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[str] = mapped_column(
        String, 
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    post_id: Mapped[str] = mapped_column(String, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)