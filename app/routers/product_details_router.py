from fastapi import Depends,APIRouter
from app.schemes import ProductData
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.product_details_service import create_products,Update_Products,delete_product_datas,get_product_details , get_all_product_details
from app.utils.auth import current_user
router = APIRouter()

@router.post("/create_product/{category_id}/{Supplier_id}")
def create_product(category_id:int,Supplier_id:int,data:ProductData, db:Session = Depends(get_db),user:User=Depends(current_user)):
    return create_products(category_id ,Supplier_id ,data , db ,user)


@router.put("/update_product/{product_id}/{supplier_id}/{category_id}")
def Update_Product(product_id:int, supplier_id:int, category_id:int, data:ProductData, db:Session=Depends(get_db),user:User=Depends(current_user)):
    return Update_Products(product_id ,supplier_id , category_id , data , db ,user)

@router.delete("/delete_product_data/{p_id}")
def delete_product_data(p_id:int,db:Session=Depends(get_db),user:User = Depends(current_user)):
    return delete_product_datas(p_id ,db ,user)

    
@router.get("/get_product_details/{p_id}")
def get_product_detail(p_id:int, db:Session=Depends(get_db)):
    return get_product_details(p_id , db)


@router.get("/get_all_product_details")
def get_all_product_detail( db:Session=Depends(get_db)):
    return get_all_product_details( db)
