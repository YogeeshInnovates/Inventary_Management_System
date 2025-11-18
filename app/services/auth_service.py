from app.models import User
from fastapi import HTTPException,Cookie
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.utils.auth import create_token
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def Signup(user, db:Session):
    db_data = db.query(User).filter(User.email == user.email).first()
    if db_data:
        raise HTTPException(status_code = 400,detail = "Email already exists")
    
    if user.role =="admin" and user.admin_code !="admin123":
        raise HTTPException(status_code=400 , detail = "Invalid admin code")
    db_user = User(
        name = user.name,
        email = user.email,
        password = pwd_context.hash(user.password),
        phone = user.phone,
        role = user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(db:Session,email:str,password:str,response):
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        raise HTTPException(status_code = 404,detail="User not found")
    
    if not pwd_context.verify(password,db_user.password):
        raise HTTPException(status_code = 400,detail="Invalid password")

    get_create_token = create_token({"sub": db_user.email}, timedelta(minutes=30))


    response.set_cookie(
    key="access_token",
    value=get_create_token,
    httponly=True,
    max_age=12*3600
        )

    return {"message":"login successfully","token":get_create_token,"token_type":"bearer"}

 