from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base

# class Base(DeclarativeBase):
#     pass


class Post(Base):
    __tablename__ = "posts"

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