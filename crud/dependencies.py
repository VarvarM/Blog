from typing import Annotated
from fastapi import Path, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Publication
from . import users
from . import publications


async def user_by_id(user_id: Annotated[int, Path],
                     session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    user = await users.get_user(session=session, user_id=user_id)
    if user is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")


async def publication_by_id(publication_id: Annotated[int, Path],
                            session: AsyncSession = Depends(db_helper.session_getter)) -> Publication:
    publication = await publications.get_publication(session=session, publication_id=publication_id)
    if publication is not None:
        return publication
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Publication {publication_id} not found")
