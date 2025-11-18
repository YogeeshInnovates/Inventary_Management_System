from sqlalchemy import Column,Integer,String,Boolean,DateTime,Text,ForeignKey , Numeric
from .database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    updated_at = Column(DateTime,default = datetime.now)

    name = Column(String(50),nullable = False)
    email = Column(String(200),unique = True,index = True,nullable = False)
    password = Column(String(200),nullable = False)
    phone = Column(String(11),nullable = False)
    role = Column(String(20),default = "user")

    pick_object = relationship("User_Pick_object", back_populates="user")
    
class Category(Base):
    __tablename__="categories"
    id = Column(Integer,primary_key = True,index=True)
    name = Column(String(100),nullable=False,unique=True)
    description = Column(String(200),nullable=True)
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime,default = datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    products = relationship("Products",back_populates = "category")

class Supplier(Base):
    __tablename__="suppliers"
    id = Column(Integer,primary_key = True,index=True)
    name= Column(String(100),nullable=False)
    contact_person = Column(String(100),nullable = True)
    email = Column(String(100),nullable = True)
    address = Column(String(200),nullable = False)
    city = Column(String(100),nullable = False)
    state = Column(String(100),nullable = False)
    country = Column(String(100),nullable = False)
    notes = Column(Text,nullable = True)
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime,default = datetime.now)
    updated_at = Column(DateTime,default = datetime.now,onupdate =datetime.now)

    products = relationship("Products",back_populates = "supplier")


class Products(Base):
    __tablename__ ="products"
    id = Column(Integer,primary_key = True,index=True)
    name = Column(String(100),nullable = False)
    category_id = Column(Integer,ForeignKey("categories.id"),nullable = False)
    Supplier_id = Column(Integer,ForeignKey("suppliers.id"),nullable = False)
    sku = Column(String(50),unique = True,nullable = False)
    price = Column(Numeric(10,2),nullable = False)
    quantity_in_stock = Column(Integer,default = 0)
    reorder_level = Column(Integer,default = 0)
    description = Column(Text,nullable = True)
    is_active = Column(Boolean,default = True)
    created_at = Column(DateTime,default =datetime.now)
    updated_at = Column(DateTime,default = datetime.now,onupdate = datetime.now)

    category = relationship("Category",back_populates = "products")
    supplier = relationship("Supplier",back_populates = "products")
    purchases = relationship("Purchase",back_populates = "product")
    sales = relationship("Sales",back_populates = "product")

     # ✅ Add this relationship line
    inventary_products = relationship(
        "Inventary_products",
        back_populates="product",
        cascade="all, delete-orphan"
    )

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer,primary_key = True,index=True)
    product_id = Column(Integer,ForeignKey("products.id"),nullable = False)
    supplier_id = Column(Integer,ForeignKey("suppliers.id"),nullable = False)
    quantity = Column(Integer,nullable = False)
    purchase_price= Column(Numeric(10,2),nullable = False)
    purchase_date = Column(DateTime,default = datetime.now)

    product = relationship("Products",back_populates = "purchases")
    supplier = relationship("Supplier")


class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer,primary_key = True,index=True)
    product_id = Column(Integer,ForeignKey("products.id"),nullable = False)
    quantity = Column(Integer,nullable = False)
    sale_price = Column(Numeric(10,2),nullable = False)
    sale_date = Column(DateTime,default = datetime.now)
    customer_name = Column(String(100),nullable = True)


    product = relationship("Products",back_populates = "sales")


class Inventary_products(Base):
    __tablename__ ="inventary_products"
    id = Column(Integer,primary_key = True,index = True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String(100),nullable = False)
    sku = Column(String(50),unique = True,nullable = False)
    quantity_in_stock = Column(Integer,default = 0)
    quantity_taken_byuser=Column(Integer,default =0)
      
    product = relationship("Products", back_populates="inventary_products")
    

class User_Pick_object(Base):
    __tablename__ = "user_pick_object"
    id = Column(Integer,primary_key = True,index = True)
    Name_of_object_taker = Column(String(50),index = True)
    product_id = Column(Integer,ForeignKey("products.id"),nullable = False)
    quantity_of_taking_product = Column(Integer,nullable = False)
    picking_date = Column(DateTime , default = datetime.now)
    user_id = Column(Integer,ForeignKey("users.id"),nullable = False)
    status_of_getting = Column(String(20),index = True)
    return_date_time = Column(DateTime)

    user= relationship("User",back_populates = "pick_object")


