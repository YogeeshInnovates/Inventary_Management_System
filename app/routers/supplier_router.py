from  fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.schemes import SupplierData
from app.services.supplier_service import create_supplieries, update_supplieries,delete_supplieries , supplier_details
from app.utils.auth import current_user
router = APIRouter()

@router.post("/create_supplier")
def create_supplier(supplier:SupplierData,db:Session = Depends(get_db),user:User = Depends(current_user)):
    return create_supplieries(supplier,db,user)

@router.put("/update_supplier/{supplier_id}")
def update_supplier(supplier_id:int,supplier:SupplierData,db:Session=Depends(get_db),user:User=Depends(current_user)):
    return  update_supplieries(supplier_id, supplier ,db ,user)


@router.delete("/delete_supplier/{supplier_id}")
def delete_supplier(supplier_id :int, db:Session = Depends(get_db),user:User=Depends(current_user)):
    return   delete_supplieries(supplier_id , db ,user)

@router.get("/supplier_details/{supplier_id}")
def supplier_detail(supplier_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    return  supplier_details(supplier_id ,db ,user)
