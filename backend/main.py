from fastapi import FastAPI

from auth.routers import users_router


app = FastAPI()

app.include_router(users_router)