from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import Optional
from random import randrange
from sqlalchemy.orm import Session
import time
from requests import post
from . import models, schemas
from .database import engine, session_local, get_db


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

@app.get("/sqlalchemy")
def get_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # return {"All Posts": posts}
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: schemas.PyDanticMediaPost, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (payload.title, payload.content, payload.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found")
    return {f"Post ID: {post_id}": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT )
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
    # post = cursor.fetchone()
    # connection.commit()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(post)
    db.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found, can't delete")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, payload: schemas.PyDanticMediaPost, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (payload.title, payload.content, payload.published, str(post_id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found, can't update")

    post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    
    return {"data": updated_post}

