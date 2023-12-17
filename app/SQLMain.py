from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
import psycopg
import time
from psycopg.rows import dict_row

from pydantic import BaseModel
from random import randrange

# from fastapi.params import Body


app = FastAPI()


class Post(BaseModel):
    title: str
    description: str
    published: bool = True


while True:
    try:
        conn = psycopg.connect(
            "host=localhost dbname=fastapi user=postgres password=Susri@221004",
            row_factory=dict_row,  # to return data as dict
        )
        cursor = conn.cursor()
        print("Database connection was succesful !!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("ERROR:", error)
        time.sleep(2)


myPosts = [
    {"id": 1, "title": "title of post1", "description": "description of post1"},
    {"id": 2, "title": "title of post2", "description": "description of post2"},
]


# def __findPost__(id):
#     for p in myPosts:
#         if p["id"] == id:
#             return p


def __findIndexOfPost__(id):
    for i, p in enumerate(myPosts):
        if p["id"] == id:
            return i


# Order of the methods matter


@app.get("/")
async def __root__():
    return {"detail": "Hello World!"}


@app.get("/posts")
async def __getPosts__():
    cursor.execute("SELECT * FROM posts ORDER BY id")
    posts = cursor.fetchall()
    return {"data": posts}


# @app.post("/createPosts")
# async def __createPosts__(payload: dict = Body(...)):
#     print(payload)
#     return {"message": "Successfully created post!", "data": {
#         "title": f"{payload["title"]}", "description": f"{payload["description"]}"
#     }}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def __createPosts__(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, description, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.description, post.published),
    )
    post = cursor.fetchone()
    conn.commit()  # to save the data to the database
    return {"detail": "Successfully created posts!", "data": post}


@app.get("/posts/latest")
def __getLatestPost__():
    post = myPosts[len(myPosts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
async def __getPost__(id: int, response: Response):
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist!",
        )

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def __deletePost__(id: int, response: Response):
    cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING *""")
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def __updatePost__(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, description = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.description, post.published, str(id)),
    )
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist.",
        )
    return {"detail": "Updated post!", "data": post}
