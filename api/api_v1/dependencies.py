from typing import Annotated
from fastapi import Path, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User
from crud import users


async def user_by_id(user_id: Annotated[int, Path],
                     session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    user = await users.get_user(session=session, user_id=user_id)
    if user is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {user_id} not found")
