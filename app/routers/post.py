from fastapi import status, Response, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils import formatPostDict
from .. import models, schemas, oauth2
from typing import Optional, List
from ..database import get_db
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


from typing import List, Optional
from fastapi.responses import JSONResponse


@router.get("/", response_model=List[schemas.PostOut])
async def __getPosts__(
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.getCurrentUser),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    results = (
        db.query(models.Post, func.count(models.Vote.postId).label("votes"))
        .join(models.Vote, models.Vote.postId == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    ).all()

    postsList = [formatPostDict(post) for post in results]

    return JSONResponse(content=postsList)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def __createPosts__(
    newPost: schemas.PostCreate,
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.getCurrentUser),
):
    # post = models.Post(
    #     title=post.title, description=post.description, published=post.published
    # )
    post = models.Post(ownerId=currentUser.id, **newPost.model_dump())

    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{id}", response_model=schemas.PostOut)
async def __getPost__(
    id: int,
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.getCurrentUser),
):
    post = (
        db.query(models.Post, func.count(models.Vote.postId).label("votes"))
        .join(models.Vote, models.Vote.postId == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found!",
        )
    return JSONResponse(formatPostDict(post))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def __deletePost__(
    id: int,
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.getCurrentUser),
):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found!",
        )

    if post.first().ownerId != currentUser.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post!",
        )
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def __updatePost__(
    id: int,
    newPost: schemas.PostCreate,
    db: Session = Depends(get_db),
    currentUser: int = Depends(oauth2.getCurrentUser),
):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found!",
        )
    if post.first().ownerId != currentUser.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post!",
        )
    post.update(newPost.model_dump(), synchronize_session=False)
    db.commit()
    return post.first()
