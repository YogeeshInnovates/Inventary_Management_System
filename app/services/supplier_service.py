from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from app.models import Supplier


def create_supplieries(supplier,db,user):
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


def update_supplieries(supplier_id, supplier ,db ,user):

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
    return {"message":"Supplier details  updated successfully"}



def delete_supplieries(supplier_id , db ,user):
    if user.role != "admin":
        raise HTTPException(status_code = 403 , detail = "You are not able to dlete this only admin can delete")
    
    db_supplier_data= db.query(Supplier).filter(Supplier.id == supplier_id).first()

    db.delete(db_supplier_data)
    db.commit()
    return {"message":"supplier deleted successfully"}

def supplier_details(supplier_id ,db ,user):
    db_supplier_data=db.query(Supplier).filter(Supplier.id == supplier_id).first()

    if db_supplier_data is None:
        raise HTTPException(status_code = 404 , detail = "No supplier info  available here")
    
    return db_supplier_data

