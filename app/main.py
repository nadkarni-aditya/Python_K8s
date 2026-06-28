from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time

from requests import post


class PyDanticMediaPost(BaseModel):
    title: str
    content: str
    published: bool = True #setting a default value if post call doesn't have this
    rating: Optional[int] = None

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


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"All Posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: PyDanticMediaPost):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (payload.title, payload.content, payload.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found")
    return {f"Post ID: {post_id}": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
    post = cursor.fetchone()
    connection.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found, can't delete")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, payload: PyDanticMediaPost):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (payload.title, payload.content, payload.published, str(post_id)))
    updated_post = cursor.fetchone()
    connection.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found, can't update")
    return {"data": updated_post}

