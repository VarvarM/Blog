from pydantic import BaseModel
from pydantic import ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: int
