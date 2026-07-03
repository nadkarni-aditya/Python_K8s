from urllib import response

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from sqlalchemy.orm import Session
import time
from requests import post
from . import models, schemas, utils
from .database import engine, session_local, get_db
from .routers import mediaposts, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
while True:
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="fastapiDB",
            user="postgres",
            password="1n33dApassword",
            cursor_factory=RealDictCursor
        )
        cursor = connection.cursor()
        print("Connected to PostgreSQL")
        break
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        time.sleep(2)

@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(mediaposts.router)
app.include_router(user.router) 







