from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from users.schemas import UserCreateSchema
from .services import register_user


users_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@users_router.post('/register', status_code=201)
async def register(user_data: UserCreateSchema, db: AsyncSession = Depends(get_session)):
    await register_user(user_data, db)

    return {'message': 'Пользователь успешно зарегистрирован!'}