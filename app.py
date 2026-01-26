from fastapi import FastAPI
from routes.user import router as user_router
from routes.auth import router as auth_router
from routes.classes import router as class_router
from db import init_db
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from middlewares import CookieToHeaderMiddleware

load_dotenv()
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Task Management API",
    description="Clean and scalable FastAPI backend demo",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(CookieToHeaderMiddleware)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(class_router)