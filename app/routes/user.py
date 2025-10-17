from typing import Union, Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session=Depends(get_db)):
    users = db.query(models.User).all()

    return users

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    print('-----create user--------', user)

    # Create has password
    hashed_password = utils.make_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} does not found!")

    return user