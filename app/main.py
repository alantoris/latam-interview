from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import User
from dotenv import load_dotenv
from app.logging import setup_logging

load_dotenv()
setup_logging()

from app.api.endpoints.user import router as user_router

app = FastAPI(
    title="User Management API",
    description="API to manage users in a secure and validated manner",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
