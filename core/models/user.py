from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .publication import Publication
    from .comment import Comment


class User(Base):
    username: Mapped[str] = mapped_column(String(17), unique=True)

    publications: Mapped[list["Publication"]] = relationship(back_populates="user")

    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
