from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .schemas import UserResponseSchema
from .models import UserModel
from .dependencies import get_current_user
from .services import get_user_by_email


users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@users_router.get('/me', response_model=UserResponseSchema)
async def get_me(payload: dict = Depends(get_current_user), db: AsyncSession = Depends(get_session)) -> UserModel:
    current_user = await get_user_by_email(payload.get('sub'), db)
    
    return current_user