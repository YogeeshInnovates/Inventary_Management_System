from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class UserCreate(BaseModel):
    name : str
    email : str
    password : str
    phone : int
    role : Optional[str] = "user"
    admin_code :Optional[str]=None

class UserResponse(BaseModel):
    id : int
    name : str
    email : str

class CategoryData(BaseModel):
    name : str
    description : str
    is_active : Optional[bool] = True
    created_at : Optional[datetime] 
    updated_at : Optional[datetime] 
 

class SupplierData(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    address: str
    city: str
    state: str
    country: str
    notes: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ProductData(BaseModel):
    name: str
    category_id: int
    Supplier_id: int
    sku: str
    price: float
    quantity_in_stock: Optional[int] = 0
    reorder_level: Optional[int] = 0
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PurchaseData(BaseModel):
   
    quantity: int
    purchase_date: Optional[datetime] = datetime.now()
    total_cost: float

class SalesData(BaseModel):
    quantity: int
    sale_date: Optional[datetime] = datetime.now()
    customer_name: str
    total_revenue: float


    class Config:
        orm_mode = True
