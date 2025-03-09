from fastapi import APIRouter, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .schemas import UserRegisterSchema, UserLoginSchema, TokenResponseSchema
from .services import register_user, authenticate_user, logout_user


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/register', status_code=201)
async def register(user_data: UserRegisterSchema, db: AsyncSession = Depends(get_session)):
    await register_user(user_data, db)

    return {'message': 'Пользователь успешно зарегистрирован!'}

@auth_router.post('/login', response_model=TokenResponseSchema)
async def login(response: Response, user: UserLoginSchema, db: AsyncSession = Depends(get_session)):
    return await authenticate_user(response, user, db)

@auth_router.post('/logout')
async def logout(response: Response):
    await logout_user(response)

    return {"message": "Вы вышли из системы"}