from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, func
from .base import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Publication(Base):
    title: Mapped[str] = mapped_column(String(52), unique=False)
    body: Mapped[str] = mapped_column(Text, server_default="")
    author: Mapped["User"] = relationship(back_populates="publication")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
