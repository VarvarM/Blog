from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from core.schemas.user import UserRead, UserCreate, UserUpdate
from crud import users as users_crud
from crud.dependencies import user_by_id

router = APIRouter(tags=["Users"])


@router.get('', response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await users_crud.get_all_users(session=session)
    return users


@router.get('/{user_id}')
async def get_user(user: User = Depends(user_by_id)):
    return user


@router.post('/create_user', response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await users_crud.create_user(session=session, user_create=user_create)
    return user


@router.put('/{user_id}', response_model=UserRead)
async def update_user(user_update: UserUpdate, user: User = Depends(user_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await users_crud.update_user(session=session, user_update=user_update, user=user)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(user_by_id), session: AsyncSession = Depends(db_helper.session_getter)):
    return await users_crud.delete_user(session=session, user=user)
