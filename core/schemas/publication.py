from datetime import datetime
from pydantic import BaseModel


class PublicationBase(BaseModel):
    title: str
    body: str
    created_at: datetime
    user_id: int


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(PublicationBase):
    pass


class PublicationRead(PublicationBase):
    id: int
