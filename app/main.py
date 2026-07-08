from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, mediaposts, user
from .config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(mediaposts.router)
app.include_router(user.router)
app.include_router(auth.router)







