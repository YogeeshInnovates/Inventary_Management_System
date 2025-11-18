from jose import jwt,JWTError
from sqlalchemy.orm import Session
from app.config import SECREATE_KEY,ALGORITHM
from fastapi import Depends,HTTPException,Cookie
from fastapi.security import  OAuth2PasswordBearer
from datetime import datetime,timedelta
from app.database import get_db
from app.models import User
auth2scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(data:dict,expire:timedelta):
    encode_data = data.copy()
    if expire:
        expire = datetime.utcnow()+expire
    else:
        expire = datetime.utcnow()+timedelta(minutes = 30)
    encode_data.update({"exp":expire})
    return jwt.encode(encode_data,SECREATE_KEY,ALGORITHM)

def verify_token(token: str):
    try:
        payload= jwt.decode(token,SECREATE_KEY,algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None
    

def current_user(token: str= Cookie(None, alias="access_token"),db:Session=Depends(get_db)):
    datas= verify_token(token)
    if datas is None:
        raise HTTPException(status_code = 401,detail = "Invalid token")
    
    user_email = datas.get("sub")
    if  user_email is None:
        raise HTTPException(status_code = 404,detail = "Invalid data")

    user = db.query(User).filter(User.email ==user_email).first()
    if user is None:
        raise HTTPException(status_code = 404,detail = "User not found")
    return user
