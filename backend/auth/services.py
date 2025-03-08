from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.schemas import UserCreateSchema
from users.models import UserModel
from .utils import hashing_password


async def get_user_by_email(user_data: UserCreateSchema, db: AsyncSession) -> UserModel | None:
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