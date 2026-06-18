from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


class PyDanticMediaPost(BaseModel):
    title: str
    content: str
    published: bool = True #setting a default value if post call doesn't have this
    rating: Optional[int] = None

app = FastAPI()

my_posts = [{"title": "First Post", "content": "This is the content of the first post.", "published": True, "rating": 5, "id": 1},
            {"title": "Second Post", "content": "This is the content of the second post.", "published": False, "rating": 3, "id": 2},
            {"title": "Third Post", "content": "This is the content of the third post.", "published": True, "rating": 4, "id": 3}]


def find_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    print(my_posts)
    return {"All Posts": my_posts}

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    # print(type(post_id))
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found")  
    print("ID: ", post_id, "Post: ", post)
    return {f"Post ID: {post_id}": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: PyDanticMediaPost):
    payload_dict = payload.model_dump()
    payload_dict["id"] = randrange(1, 100000)
    print(payload.model_dump())
    my_posts.append(payload_dict)
    return {"data": payload.model_dump()}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found, can't delete")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, payload: PyDanticMediaPost):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} not found, can't update")
    payload_dict = payload.model_dump()
    payload_dict["id"] = post_id
    post.update(payload_dict)  # ✅ Update the dict, not the list
    return {"data": post}

