from fastapi import status, HTTPException, Depends, APIRouter, Response
from database import get_db
from sqlalchemy.orm import Session
import models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(
    tags=['Authorization']
)



@router.post('/login')
#using OAuth2Password allows form data
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        #if user does not equal user in DB then invalid
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid creds")
    #if password does not equal password in DB then invalid
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, details=f"invalid creds")
    

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"token": access_token, "token_type": "bearer"}
