import pytest
from unittest.mock import MagicMock
from app.services.product_sales_service import create_sales_records,update_sales_records,view_all_sales_datas,delete_sales_datas
from datetime import datetime
from fastapi import HTTPException
@pytest.fixture
def mock_db():
    session = MagicMock()
    return session


class products:
    product_id = 1           # Add this
    quantity = 2             # Add this
    total_revenue = 20000    # Add this
    sale_date = datetime.now()
    customer_name = "Ram"
    name = "resberryphi"
    category_id = 1
    Supplier_id = 1
    sku = "RES34"
    price = 10000
    quantity_in_stock = 10
    reorder_level = 2
    description = "used to prepare intelligent ai model"
    is_active = True
    created_at = datetime.now()
    updated_at = datetime.now()


class fakeUser:
    id = 1
    name = "Ram"
    email ="Ram@gmail.com"
    password  = "ram@1234"
    phone = 9354231414
    role = "user"


class Fake_admin:
    id = 1
    name = "Shiva"
    email ="Ram@gmail.com"
    password = "ram@1234"
    phone = 9354231414
    role = "admin"
    admin_code = "admin123"


class Salesdata:
    id = 1
    product_id = 1
    quantity = 2
    sale_price =10000
    sale_date = datetime.now()
    customer_name = "Ram"


class updated_Salesdata:
    id = 1
    product_id = 1
    quantity = 2
    total_revenue =100     # <- this matches the service function
    sale_date = datetime.now()
    customer_name = "Ramesh"


def test_create_sales_records(mock_db):
    admin = Fake_admin()
    user = fakeUser()
    data = products()


    result = create_sales_records(1, data , mock_db ,admin)

    assert result["message"] ==  "Create sales record successfully"

    with pytest.raises(HTTPException) as exec:
        create_sales_records(1, data , mock_db ,user)
    assert exec.value.status_code == 403
    assert exec.value.detail ==  "Only admin can handel this "


def test_update_sales_records_check(mock_db):
    admin = Fake_admin()
    user = fakeUser()
    data = Salesdata()
    product_id = 1

    sales_datas = updated_Salesdata()

    mock_db.query.return_value.filter.return_value.first.return_value = data
    # mock_db.query.return_value.filter.return_value.first.return_value = Salesdata()

    result = update_sales_records(product_id, sales_datas, mock_db, admin)

    updated = mock_db.query.return_value.filter.return_value.first.return_value

    assert updated.sale_price == 100
    assert updated.customer_name == "Ramesh"
    assert result["message"] == "Update sales record successfully"

    with pytest.raises(HTTPException) as exec:
        update_sales_records(product_id ,sales_datas ,mock_db ,user)
        
    assert exec.value.status_code == 403
    assert exec.value.detail == "Only admin can hndel sales data"

    
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exec:
        update_sales_records(product_id ,sales_datas ,mock_db ,admin)
    
    assert exec.value.status_code == 404
    assert exec.value.detail == "No saels record on this product"



def test_view_all_sales_datas_check(mock_db):

    admin = Fake_admin()
    user = fakeUser()
    data = Salesdata()
    product_id = 1

    sales_datas = updated_Salesdata()

    mock_db.query.return_value.all.return_value = data

    result = view_all_sales_datas(mock_db)
    assert result.customer_name == "Ram"


def test_delete_sales_datas_check(mock_db):
    admin = Fake_admin()
    user = fakeUser()
    data = Salesdata()
    sales_id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = data 

    result = delete_sales_datas(sales_id ,mock_db , admin )

    assert result["message"] == "deleted successfully"

    with pytest.raises(HTTPException) as exec:
        delete_sales_datas(sales_id ,mock_db , user )
    
    assert exec.value.status_code == 403
    assert exec.value.detail == "only admin can delete sales data"






# def create_sales_records( data , db ,user):
#     if user != "admin":
#         raise HTTPException(status_code = 403, detail = "Only admin can handel this ")
    
#     sales_data= Sales(
#     product_id = data.product_id,
#     quantity = data.quantity,
#     sale_price = data.total_revenue,
#     sale_date = data.sale_date,
#     customer_name = data.customer_name
#     )

#     db.add(sales_data)
#     db.commit()
#     db.refresh(sales_data)
#     return {"message":"Create sales record successfully"}

# def update_sales_records(product_id ,data ,db ,user):

#     if user != "admin":
#         raise HTTPException (status_code = 403, detail = "Only admin can hndel sales data")
#     sales_data = db.query(Sales).filter(Sales.product_id == product_id).first()

#     if not sales_data:
#         raise HTTPException(status_code = 404, detail = "No saels record on this product")

#     sales_data.product_id = data.product_id,
#     sales_data.quantity = data.quantity,
#     sales_data.sale_price = data.total_revenue,
#     sales_data.sale_date = data.sale_date,
#     sales_data.customer_name = data.customer_name

#     db.add(sales_data)
#     db.commit()
#     db.refresh(sales_data)
#     return {"message":"Update sales record successfully"}
 

# def view_all_sales_datas(db):
#     sales_data=db.query(Sales).all()
#     return sales_data


# def delete_sales_datas(sales_id ,db , user ):
#     if user.role !="admin":
#         raise HTTPException(status_code= 403,detail = "only admin can delete sales data")

#     sales_data = db.query(Sales).filter(Sales.id == sales_id).first()

#     db.delete(sales_data)
#     db.commit()
#     db.refresh(sales_data)

#     return {"message":"deleted successfully"}

