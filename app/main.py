from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from app.database import SessionLocal,engine
from app.schemes import UserCreate,UserResponse,CategoryData,SupplierData,ProductData,PurchaseData,SalesData
from app.models import User,Category,Supplier,Products,Purchase,Sales
from sqlalchemy import text
from passlib.context import CryptContext
from jose import jwt,JWTError

from app.config import SECREATE_KEY,ALGORITHM,EXPIRE_MINUTES
from datetime import datetime ,timedelta
pwd_context = CryptContext(schemes =["bcrypt"],deprecated = "auto")
app = FastAPI()

auth2scheme = OAuth2PasswordBearer(tokenUrl="/login")
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    

def current_user(token:str = Depends(auth2scheme),db:Session=Depends(get_db)):
    datas= verify_token(token)
    if datas is None:
        raise HTTPException(status_code = 404,detail = "Invalid data")
    
    user_email = datas.get("sub")
    if  user_email is None:
        raise HTTPException(status_code = 404,detail = "Invalid data")

    user = db.query(User).filter(User.email ==user_email).first()
    if user is None:
        raise HTTPException(status_code = 404,detail = "User not found")
    return user


@app.get("/")
def home(db:Session=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message":"Database connection successfully"}
    except Exception as e:
        return {"message":"Database connection failed","error":str(e)}

@app.post("/signup",response_model = UserResponse)
def Signup(user:UserCreate, db:Session=Depends(get_db)):
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

@app.post("/login")
def login(email: str,password:str,db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        raise HTTPException(status_code = 404,detail="User not found")
    
    if not pwd_context.verify(password,db_user.password):
        raise HTTPException(status_code = 400,detail="Invalid password")

    get_create_token = create_token({"sub": db_user.email}, timedelta(minutes=30))


    return {"message":"login successfully","token":get_create_token,"token_type":"bearer"}

 
@app.post("/create_category")
def Create_category(category:CategoryData,db:Session=Depends(get_db),user:User=Depends(current_user)):
    if user.role != "admin":
        raise HTTPException(status_code = 403,detail = "You are not access to this only admins can handel the category")
    
    db_category= Category(
       
    name = category.name,
    description = category.description,
    is_active = category.is_active,
    created_at = category.created_at,
    updated_at = category.updated_at
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return {"message":"Category created successfully"}


@app.put("/update_category/{category_id}")
def update_category(category_id:int,category:CategoryData,db:Session = Depends(get_db),user:User = Depends(current_user)):
    if user.role != "admin":
        raise HTTPException(status_code = 403,detail = "You are not allow to access  ,only admin can modify the data")
    
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code = 404,detail ="No category present with this name")
    db_category.name = category.name
    db_category.description = category.description,
    db_category.is_active = category.is_active,
    db_category.created_at = category.created_at,
    db_category.updated_at = category.updated_at

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return {"message":"updated successfully"}

@app.get("/get_category/{category_id}")
def get_category(category_id : int, category:CategoryData,db :Session=Depends(get_db),user:User=Depends(current_user)):
    category_datas=db.query(Category).filter(Category.id == category_id).first()

    if category_datas is None:
        raise HTTPException(status_code = 404,detail = "No category details available on this id")
    
    return category_datas

@app.delete("delete_category/{category_id}")
def delete_category(category_id:int,db:Session=Depends(get_db),user :User = Depends(current_user)):
    if user.role != "admin":
        raise HTTPException(status_code = 403 , detail = "You are not allowed to access this ,only admin can  delete")
    
    db_category_data = db.query(Category).filter(Category.id == category_id).first()

    if not db_category_data:
        raise HTTPException( status_code = 404 , detail = "No category available on thi s id ")
    db.delete(db_category_data)
    db.commit()

    return {"message":"Category deleted successfully"}



@app.post("/create_supplier")
def create_supplier(supplier:SupplierData,db:Session = Depends(get_db),user:User = Depends(current_user)):
    if user.role != "admin":
        
        raise HTTPException(status_code = 403 , detail = "You are not allowed to access for this id only admin can  insert details")
    
    db_supplier = Supplier(

    name= supplier.name,
    contact_person = supplier.contact_person,
    email = supplier.email,
    address = supplier.address,
    city = supplier.city,
    state = supplier.state,
    country = supplier.country,
    notes = supplier.notes,
    is_active = supplier.is_active,
    created_at =supplier.created_at,
    updated_at = supplier.updated_at,
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    return {"message":"supplier entries done succcessfully"}


@app.put("/update_supplier/{supplier_id}")
def update_supplier(supplier_id:int,supplier:SupplierData,db:Session=Depends(get_db),user:User=Depends(current_user)):

    if user.role != "admin":
        raise HTTPException(status_code = 403, detail = "You are not allowed to update this only admin can update")
    
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()

    if not db_supplier:
        raise HTTPException(status_code = 404, detail = "NO supplier available on this id")
    
    db_supplier.name= supplier.name
    db_supplier.contact_person = supplier.contact_person
    db_supplier.email = supplier.email
    db_supplier.address = supplier.address
    db_supplier.city = supplier.city
    db_supplier.state = supplier.state
    db_supplier.country = supplier.country
    db_supplier.notes = supplier.notes
    db_supplier.is_active = supplier.is_active
    db_supplier.created_at =supplier.created_at
    db_supplier.updated_at = supplier.updated_at

    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

@app.delete("/delete_supplier/{supplier_id}")
def delete_supplier(supplier_id :int, db:Session = Depends(get_db),user:User=Depends(current_user)):
    if user.role != "admin":
        raise HTTPException(sttaus_code = 403 , detail = "You are not able to dlete this only admin can delete")
    
    db_supplier_data= db.query(Supplier).filter(Supplier.id == supplier_id).first()

    db.delete(db_supplier_data)
    db.commit()
    return {"message":"supplier deleted successfully"}

@app.get("/supplier_details/{supplier_id}")
def supplier_details(supplier_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    db_supplier_data=db.query(Supplier).filter(Supplier.id == supplier_id).first()

    if db_supplier_data is None:
        raise HTTPException(status_cide = 404 , detail = "No supplier info  available here")
    
    return db_supplier_data



