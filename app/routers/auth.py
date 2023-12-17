from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def __login__(
    userCredentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    # username = userCredentials.username (instead of email)
    # password = userCredentials.password
    user = (
        db.query(models.User)
        .filter(models.User.email == userCredentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!"
        )

    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!"
        )

    accessToken = oauth2.createAccessToken(data={"userId": user.id})
    return {"accessToken": accessToken, "tokenType": "bearer"}


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
async def __register__(
    newUser: schemas.UserCreate, db: Session = Depends(database.get_db)
):
    newUser.password = utils.hash(newUser.password)
    user = models.User(**newUser.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
