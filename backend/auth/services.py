from sqlalchemy.ext.asyncio import AsyncSession

from users.schemas import UserCreateSchema


async def register_user(user_data: UserCreateSchema, db: AsyncSession):
    pass