from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .schemas import UserResponseSchema
from .models import UserModel
from .services import get_current_user


users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@users_router.get('/me', response_model=UserResponseSchema)
async def get_me(access_token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)) -> UserModel:
    current_user = await get_current_user(access_token, db)
    
    return current_user