from jose import JWTError, jwt  
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os


load_dotenv(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


#scheme used to define the authentication method for endpoints using OAuth2 with a password
#OAuth2 class takes tokenUrl which specifices where the user goes to retrieve a token, /login
oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#token ingredients
# SECRET_KEY = "1ae0833d77ac0d723d024b8b6f148a25bd05d66783864b868877214c034fc9f7"
# ALGORITHIM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

#create access token
def create_access_token(data: dict):
    #make a copy of data so we don't change original value, and encode it
    to_encode = data.copy()
    #expiration field, need current and future time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#verify access token
#consuming token and secret (credentials_exception)
def verify_access_token(token: str, credentials_exception):
    
    try:
        #remember we want to decode the 3 ingredients that make the token
        #returns a dictionary-like object containing the decoded payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #extract the user ID from this decoded payload
        #if there is no ID then raise exception
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        #saving the user ID in token_data because we have an ID
        #saving the ID in token_data then valiate it against schema
        #if it does not comply with schema then raise exception 
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    

#dependency function used to get current authenticated user via access token
#token is parameter obtained from the header, you can see it in the JSON    
#token gets the access token via oath2 scheme 
def get_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"creds aren't valid", headers={"WWW-Authenticate": "Bearer"})

    #if the token is valid and the user is successfully authenticated
    token = verify_access_token(token, credentials_exception)
    return (token.id)



