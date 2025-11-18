from fastapi import Depends , APIRouter
from sqlalchemy.orm import Session
from app.schemes import SalesData
from app.database import get_db
from app.models import User
from app.utils.auth import current_user
from app.services.product_sales_service import create_sales_records,update_sales_records,view_all_sales_datas,delete_sales_datas

router = APIRouter()
@router.post("/create_sales_record/{product_id}")
def create_sales_record(product_id:int, data:SalesData, db:Session=Depends(get_db),user:User=Depends(current_user)):
    return create_sales_records( product_id,data , db ,user)


@router.put("/update_sales_record/{product_id}")
def update_sales_record(product_id:int ,data:SalesData ,db:Session=Depends(get_db),user:User=Depends(current_user)):
    return update_sales_records(product_id ,data ,db ,user)
  

@router.get("/view_all_sales_data")
def view_all_sales_data(db:Session=Depends(get_db)):
    return  view_all_sales_datas(db)

@router.delete("/delete_sales_data/{sales_id}")
def delete_sales_data(sales_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    return delete_sales_datas(sales_id ,db , user )