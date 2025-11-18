from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.inventary_details_service import GetInventary_detail
router = APIRouter()

@router.get("/GetInventary_details")
def GetInventary_details(db:Session=Depends(get_db)):
    return  GetInventary_detail(db)


