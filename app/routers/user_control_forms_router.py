from fastapi import Depends ,APIRouter
from app.models import User
from app.database import get_db
from app.schemes import Users_Pick_objects
from sqlalchemy.orm import Session
from app.services.user_control_forms_service import  User_return_Datas,User_Picking_Datas,getProductcarryUser_details
from app.utils.auth import current_user


router = APIRouter()

@router.post("/User_Picking_Data/{product_id}")
def User_Picking_Data(product_id :int ,data: Users_Pick_objects,db:Session=Depends(get_db),user:User = Depends(current_user)):
    return User_Picking_Datas(product_id ,data ,db ,user)


@router.post("/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}")
def User_return_Data(product_id:int,quantity_of_return_product:int,status_usage: str ,db:Session=Depends(get_db),user:User=Depends(current_user)):
    return User_return_Datas(product_id ,quantity_of_return_product ,status_usage  ,db ,user )



@router.get("/getProductcarryUser_details")
def getProductcarryUser_detail(db:Session=Depends(get_db)):
    return getProductcarryUser_details(db)
   