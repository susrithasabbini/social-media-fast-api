from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    currentUser: int = Depends(oauth2.getCurrentUser),
):
    post = db.query(models.Post).filter(models.Post.id == vote.postId).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {vote.postId} does not exist",
        )
    voteQuery = db.query(models.Vote).filter(
        models.Vote.postId == vote.postId, models.Vote.userId == currentUser.id
    )
    foundVote = voteQuery.first()
    if vote.dir == 1:
        if foundVote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {currentUser.id} already voted on post {vote.postId}",
            )
        newVote = models.Vote(postId=vote.postId, userId=currentUser.id)
        db.add(newVote)
        db.commit()
        return {"detail": "Successfully added your vote"}
    else:
        if not foundVote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist"
            )
        voteQuery.delete(synchronize_session=False)
        db.commit()
        return {"detail": "Successfully removed your vote"}
