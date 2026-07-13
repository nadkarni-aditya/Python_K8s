from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, mediaposts, user, vote
from .config import settings


# models.Base.metadata.create_all(bind=engine) don't need to be called here because we are using Alembic for migrations

app = FastAPI()


app.include_router(mediaposts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)







