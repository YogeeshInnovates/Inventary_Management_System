from fastapi import APIRouter,Depends,HTTPException,Response
from app.schemes import UserCreate,UserResponse,CategoryData,SupplierData,ProductData,PurchaseData,SalesData,Users_Pick_objects
from app.models import User,Category,Supplier,Products,Purchase,Sales,User_Pick_object,Inventary_products
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import  Signup,login_user
router = APIRouter()

@router.post("/signup")
def signup_route(user:UserCreate, db:Session=Depends(get_db)):
    return Signup(user,db)

@router.post("/login")
def login(email: str,password:str,response:Response, db:Session = Depends(get_db)):
    return login_user(db,email,password,response)