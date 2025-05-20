from fastapi import FastAPI
from app.db.database import Base, engine
from dotenv import load_dotenv

load_dotenv()

#from app.routers import user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

#app.include_router(user_router)