
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, session_local, get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"] 
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PyDanticResponseUser)
def create_user(CreateUserPayload: schemas.PyDanticCreateUser, db: Session = Depends(get_db)):

    CreateUserPayload.password = utils.hash_password(CreateUserPayload.password)

    new_user = models.User(**CreateUserPayload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=schemas.PyDanticResponseUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID {user_id} not found")
    return user