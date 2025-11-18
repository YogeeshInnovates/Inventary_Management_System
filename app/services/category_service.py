from fastapi import HTTPException
from app.models import Category
from sqlalchemy.orm import Session

def Create_categories(db:Session,category,user):
    if user.role != "admin":
        raise HTTPException(status_code = 403,detail = "You are not access to this only admins can handel the category")
    
    db_category= Category(
       
    name = category.name,
    description = category.description,
    is_active = category.is_active,
    created_at = category.created_at,
    updated_at = category.updated_at
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return {"message":"Category created successfully"}


def update_categories(category_id,category,db,user):
    if user.role != "admin":
        raise HTTPException(status_code = 403,detail = "You are not allow to access  ,only admin can modify the data")
    
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code = 404,detail ="No category present with this name")
    db_category.name = category.name
    db_category.description = category.description
    db_category.is_active = category.is_active
    db_category.created_at = category.created_at
    db_category.updated_at = category.updated_at


    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return {"message":"updated successfully"}



def get_categories(category_id ,db ,user):
    category_datas=db.query(Category).filter(Category.id == category_id).first()

    if category_datas is None:
        raise HTTPException(status_code = 404,detail = "No category details available on this id")
    
    return category_datas

def delete_categories(category_id, db ,user ):
    if user.role != "admin":
        raise HTTPException(status_code = 403 , detail = "You are not allowed to access this ,only admin can  delete")
    
    db_category_data = db.query(Category).filter(Category.id == category_id).first()

    if not db_category_data:
        raise HTTPException( status_code = 404 , detail = "No category available on thi s id ")
    db.delete(db_category_data)
    db.commit()

    return {"message":"Category deleted successfully"}

