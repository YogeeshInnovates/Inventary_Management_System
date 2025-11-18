from fastapi import HTTPException,APIRouter,Depends
from app.schemes import CategoryData
from app.database import get_db
from app.models import User
from app.utils.auth import current_user
from sqlalchemy.orm import Session
from app.services.category_service import Create_categories,update_categories,get_categories,delete_categories
router = APIRouter()

@router.post("/create_category")
def Create_category(category:CategoryData,db:Session=Depends(get_db),user:User=Depends(current_user)):
    return Create_categories(db,category,user)
   

@router.put("/update_category/{category_id}")
def update_category(category_id:int,category:CategoryData,db:Session = Depends(get_db),user:User = Depends(current_user)):
    return update_categories(category_id,category,db,user)

@router.get("/get_category/{category_id}")
def get_category(category_id : int,db :Session=Depends(get_db),user:User=Depends(current_user)):
    return get_categories(category_id ,db ,user)


@router.delete("/delete_category/{category_id}")
def delete_category(category_id:int,db:Session=Depends(get_db),user :User = Depends(current_user)):
    return delete_categories(category_id, db ,user )
