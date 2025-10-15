from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(tags=['Authentication'])



@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session=Depends(get_db)):
    
    auth_user = db.query(models.User).filter(models.User.email == user_credentials.email)

    if not auth_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials.')
    
    if not utils.verify_password(user_credentials.password, auth_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials.')
    
    # create token