from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


7.28

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session=Depends(get_db)):
    
    auth_user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not auth_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials.')
    
    if not utils.verify_password(user_credentials.password, auth_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials.')
    
    access_token = oauth2.create_access_token(data={"user_id": auth_user.id})
    
    # create a token
    return {'access_token': access_token, 'token_type': "bearer"}