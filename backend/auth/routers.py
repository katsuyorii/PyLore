from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .schemas import UserRegisterSchema, UserLoginSchema, TokenResponseSchema
from .services import register_user, authenticate_user


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/register', status_code=201)
async def register(user_data: UserRegisterSchema, db: AsyncSession = Depends(get_session)):
    await register_user(user_data, db)

    return {'message': 'Пользователь успешно зарегистрирован!'}

@auth_router.post('/login', response_model=TokenResponseSchema)
async def login(user: UserLoginSchema, db: AsyncSession = Depends(get_session)):
    return await authenticate_user(user, db)