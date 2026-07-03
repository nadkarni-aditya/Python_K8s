from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app import schemas, models, utils, database

router = APIRouter(tags = ["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(usercreds: schemas.userlogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == usercreds.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not utils.verify_password(usercreds.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    return {"token": "example_token", "token_type": "bearer"}