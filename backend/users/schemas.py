import re

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from datetime import datetime, date

from .models import UserRole


REGEX_USERNAME = re.compile(r"^(?=.{1,128}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$")

REGEX_NAMES = re.compile(r"^[a-zA-Zа-яА-Я ,.'-]+$")

REGEX_PASSWORD = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")

class BaseORMSchema(BaseModel):
    ''' Base schema class for convert to json (ORM) '''
    model_config = ConfigDict(from_attributes=True)

class UserResponseSchema(BaseORMSchema):
    id: int
    email: EmailStr
    username: str
    role: UserRole
    first_name: str | None
    last_name: str | None
    date_of_birth: date | None
    is_active: bool
    created_at: datetime

class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str | None = Field(default=None, max_length=128)
    last_name: str | None = Field(default=None, max_length=128)
    date_of_birth: date | None = Field(default=None)

    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, value):
        if not REGEX_USERNAME.match(value):
            raise HTTPException(
                status_code=422,
                detail="Username должен быть от 8 до 128 символов, может содержать только латинские буквы, цифры, '_', '.', и не может начинаться или заканчиваться на '_' или '.'"
            )
        return value
    
    @field_validator('first_name', mode='before')
    @classmethod
    def validate_first_name(cls, value):
        if not REGEX_NAMES.match(value):
            raise HTTPException(
                status_code=422,
                detail="Имя и фамилия могут содержать только буквы, пробелы, апострофы, дефисы и точки. Цифры и спецсимволы запрещены."
            )
        return value
    
    @field_validator('last_name', mode='before')
    @classmethod
    def validate_last_name(cls, value):
        if not REGEX_NAMES.match(value):
            raise HTTPException(
                status_code=422,
                detail="Имя и фамилия могут содержать только буквы, пробелы, апострофы, дефисы и точки. Цифры и спецсимволы запрещены."
            )
        return value
    
    @field_validator('password', mode='before')
    @classmethod
    def validate_password(cls, value):
        if not REGEX_PASSWORD.match(value):
            raise HTTPException(
                status_code=422,
                detail="Пароль должен содержать минимум 8 символов, хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ (#?!@$%^&*-)."
            )
        print(value)
        return value