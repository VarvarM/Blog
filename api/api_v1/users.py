from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.schemas.user import UserRead, UserCreate, UserUpdate, UserBase
from crud.users import get_all_users
from crud import users as users_crud
from crud.dependencies import user_by_id

router = APIRouter(tags=["Users"])


@router.get('', response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await get_all_users(session=session)
    return users


@router.post('/create_user', response_model=UserRead)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await users_crud.create_user(session=session, user_create=user_create)
    return user


@router.put('/{user_id}', response_model=UserRead)
async def update_user(user_update: UserUpdate, user: User = Depends(user_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await users_crud.update_user(session=session, user_update=user_update, user=user)


@router.delete('/{user_id}')
async def delete_user(user: UserBase = Depends(user_by_id), session: AsyncSession = Depends(db_helper.session_getter)):
    return await users_crud.delete_user(session=session, user=user)
