from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any

from users.schemas import UserCreateSchema, UserLoginSchema
from users.models import UserModel
from .utils import hashing_password, verify_password, create_access_token
from .schemas import TokenResponseSchema


async def get_user_by_email(user_data: Any, db: AsyncSession) -> UserModel | None:
    result = await db.execute(select(UserModel).where(UserModel.email == user_data.email))
    return result.scalars().one_or_none()

async def register_user(user_data: UserCreateSchema, db: AsyncSession):
    existing_user = await get_user_by_email(user_data, db)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail='Пользователь с таким email уже существует!'
        )

    user_data_dict = user_data.model_dump()
    user_data_dict['password'] = hashing_password(user_data.password)

    user = UserModel(**user_data_dict)
    db.add(user)
    await db.flush()
    await db.commit()

async def authenticate_user(user: UserLoginSchema, db: AsyncSession) -> TokenResponseSchema:
    existing_user = await get_user_by_email(user, db)

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail='Неверный адрес электронный почты или пароль!'
        )
    
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail='Неверный адрес электронный почты или пароль!'
        )
    
    access_token = create_access_token({
        'sub': existing_user.email,
        'username': existing_user.username,
        'role': existing_user.role,
    })

    return TokenResponseSchema(access_token=access_token, token_type='bearer')