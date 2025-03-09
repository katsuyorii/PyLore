from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel


async def get_user_by_email(email: str, db: AsyncSession) -> UserModel | None:
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    return result.scalars().one_or_none()