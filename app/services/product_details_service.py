from fastapi import HTTPException
from app.models import Products ,Inventary_products
from datetime import datetime,timedelta

def create_products(category_id ,Supplier_id ,data , db ,user):

    if user.role !="admin":
        raise HTTPException (status_code = 403,detail = "You are not allowed to create product detail table  only admins can handel it ")
    
     
    Product_datas=Products(
    name = data.name,
    category_id =data.category_id,
    Supplier_id =data.Supplier_id,
    sku = data.sku,
    price = data.price,
    quantity_in_stock = data.quantity_in_stock,
    reorder_level = data.reorder_level,
    description = data.description,
    is_active = data.is_active,
    created_at = datetime.now(),
    updated_at = datetime.now()
    )

    db.add(Product_datas)
    db.commit()
    db.refresh(Product_datas)

    inventary_data = Inventary_products(
    product_id = Product_datas.id,
    name = Product_datas.name,
    sku = Product_datas.sku,
    quantity_in_stock =Product_datas.quantity_in_stock
   
    )

    db.add(inventary_data)
    db.commit()
    db.refresh(inventary_data)

    return {"message":"Your product details are enter successfully"}




def Update_Products(product_id ,supplier_id , category_id , data , db ,user):
    get_db_data = db.query(Products).filter(Products.id == product_id).first()

    if user.role !="admin":
        raise HTTPException(status_code = 403,detail = "only admin can handel  this")
    
    if not get_db_data:
        raise HTTPException(status_code=404 ,detail = "you entered wrong product which is not available")
    
    get_db_data.name = data.name
    get_db_data.category_id =data.category_id
    get_db_data.Supplier_id =data.Supplier_id
    get_db_data.sku = data.sku
    get_db_data.price = data.price
    get_db_data.quantity_in_stock = data.quantity_in_stock
    get_db_data.reorder_level = data.reorder_level
    get_db_data.description = data.description
    get_db_data.is_active = data.is_active
    get_db_data.updated_at = datetime.now()

    db.add(get_db_data)
    db.commit()
    db.refresh(get_db_data)

    inventary_data = db.query(Inventary_products).filter(Inventary_products.product_id == product_id).first()

    inventary_data.name = get_db_data.name
    inventary_data.sku = get_db_data.sku
    inventary_data.quantity_in_stock =get_db_data.quantity_in_stock

    db.add(inventary_data)
    db.commit()
    db.refresh(inventary_data)
    return {"message":"Successfully updated"}
    
def delete_product_datas(p_id ,db ,user):
    if user.role != "admin":
        raise HTTPException(status_code= 403, detail="User not allow to delete product ,so only admn can handel this")
    
    product_data = db.query(Products).filter(Products.id == p_id).first()
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")


    
    inventary_data = db.query(Inventary_products).filter(Inventary_products.product_id == p_id).first()

    if inventary_data:
        db.delete(inventary_data)

    # ✅ Then delete product
    db.delete(product_data)
    db.commit()


    return {"message":"deleted successfully"}

    
def get_product_details(p_id , db):
    db_product = db.query(Products).filter(Products.id == p_id).first()

    if not db_product:
        raise HTTPException(status_code=404 , detail = "no product available ")
    return db_product


def get_all_product_details( db):
    db_product = db.query(Products).all()
     
    if not db_product:
        raise HTTPException(status_code=404 , detail = "no product available ")
    return db_product
