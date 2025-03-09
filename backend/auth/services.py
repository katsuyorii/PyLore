from fastapi import HTTPException, Response, Request

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import timedelta

from src.config import settings
from .schemas import UserRegisterSchema, UserLoginSchema, TokenResponseSchema
from .utils import hashing_password, verify_password, create_access_token, create_refresh_token, verify_refresh_token
from users.models import UserModel
from users.services import get_user_by_email


async def register_user(user_data: UserRegisterSchema, db: AsyncSession):
    existing_user = await get_user_by_email(user_data.email, db)

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

async def authenticate_user(response: Response, user: UserLoginSchema, db: AsyncSession) -> TokenResponseSchema:
    existing_user = await get_user_by_email(user.email, db)

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

    refresh_token = create_refresh_token({
        'sub': existing_user.email,
        'username': existing_user.username,
        'role': existing_user.role,
    })

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        max_age=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        samesite='Strict',
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        max_age=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        samesite='Strict',
    )

    return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token, token_type='bearer')

async def logout_user(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token отсутствует"
        )
    
    payload = verify_refresh_token(refresh_token)

    new_access_token = create_access_token(payload)

    response.set_cookie(
        key='access_token',
        value=new_access_token,
        httponly=True,
        max_age=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        samesite='Strict',
    )

    return TokenResponseSchema(access_token=new_access_token, refresh_token=refresh_token, token_type='bearer')