from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, func, ForeignKey
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .publication import Publication


class Comment(Base):
    body: Mapped[str] = mapped_column(Text, server_default="")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"))
    publication: Mapped["Publication"] = relationship(back_populates="comments")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="comments")

