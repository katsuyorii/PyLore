from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import verify_access_token
from .models import UserModel


async def get_current_user(access_token: str, db: AsyncSession) -> UserModel:
    payload = verify_access_token(access_token)
    email = payload.get('sub')

    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalars().first()

    return user