from fastapi import HTTPException
from app.models import  Sales

def create_sales_records(product_ids,data , db ,user):
    if user.role != "admin":
        raise HTTPException(status_code = 403, detail = "Only admin can handel this ")
    
    sales_data= Sales(
    product_id = product_ids,
    quantity = data.quantity,
    sale_price = data.total_revenue,
    sale_date = data.sale_date,
    customer_name = data.customer_name
    )

    db.add(sales_data)
    db.commit()
    db.refresh(sales_data)
    return {"message":"Create sales record successfully"}

def update_sales_records(product_id ,data ,db ,user):

    if user.role != "admin":
        raise HTTPException (status_code = 403, detail = "Only admin can hndel sales data")
    sales_data = db.query(Sales).filter(Sales.product_id == product_id).first()

    if not sales_data:
        raise HTTPException(status_code = 404, detail = "No saels record on this product")

    sales_data.product_id = product_id
    sales_data.quantity = data.quantity
    sales_data.sale_price = data.total_revenue
    sales_data.sale_date = data.sale_date
    sales_data.customer_name = data.customer_name

    db.add(sales_data)
    db.commit()
    db.refresh(sales_data)
    return {"message":"Update sales record successfully"}
 

def view_all_sales_datas(db):
    sales_data=db.query(Sales).all()
    return sales_data


def delete_sales_datas(sales_id ,db , user ):
    if user.role !="admin":
        raise HTTPException(status_code= 403,detail = "only admin can delete sales data")

    sales_data = db.query(Sales).filter(Sales.id == sales_id).first()

    db.delete(sales_data)
    db.commit()

    return {"message":"deleted successfully"}

