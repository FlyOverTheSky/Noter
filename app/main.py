from fastapi import FastAPI
from .database import engine
from app.database import Base
from app.routes import notes, users
from app.utils.logger import setup_logger

app = FastAPI(title="Noter")
Base.metadata.create_all(bind=engine)
setup_logger()

app.include_router(users.router)
app.include_router(notes.router)