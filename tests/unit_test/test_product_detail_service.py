from fastapi import HTTPException
import pytest
from unittest.mock import MagicMock
from app.services.product_details_service import create_products , Update_Products,delete_product_datas,get_product_details,get_all_product_details
from datetime import datetime
@pytest.fixture
def mock_db():
    session = MagicMock()
    return session


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

class products:
        id = 1
        name = "resberryphi"
        category_id =1
        Supplier_id = 1
        sku = "RES34"
        price =  10000
        quantity_in_stock = 10
        reorder_level = 2
        description = "used to prepare intelligent ai model"
        is_active = "True"
        created_at = datetime.now(),
        updated_at = datetime.now()

def test_create_products(mock_db):
    user =  fakeUser()
    admins = Fake_admin()
    data = products()
    category_id = 1
    Supplier_id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = data

    result =  create_products(category_id ,Supplier_id ,data , mock_db ,admins)

    assert result["message"] ==  "Your product details are enter successfully"
    
    mock_db.query.return_value.filter.return_value.first.return_value = data

    with pytest.raises(HTTPException) as exec:
        create_products(category_id ,Supplier_id ,data , mock_db ,user)
    
    assert exec.value.status_code == 403
    assert exec.value.detail ==  "You are not allowed to create product detail table  only admins can handel it "

def test_Update_Products_check(mock_db):
    user =  fakeUser()
    admins = Fake_admin()
    data = products()
    category_id = 1
    supplier_id = 1
    product_id  = 1
    

    mock_db.query.return_value.filter.return_value.first.return_value = data

    result = Update_Products(product_id ,supplier_id , category_id , data , mock_db ,admins)

    assert result["message"] =="Successfully updated"

    # wrong product ids
    product_ids  = 2
    

    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exec:
        Update_Products(product_ids ,supplier_id , category_id , data , mock_db ,admins)

    assert exec.value.status_code == 404
    assert exec.value.detail ==  "you entered wrong product which is not available"

    

    mock_db.query.return_value.filter.return_value.first.return_value = data
    # nonadmin try to update
    with pytest.raises(HTTPException) as exec:
        Update_Products(product_id ,supplier_id , category_id , data , mock_db ,user)
    
    assert exec.value.status_code == 403
    assert exec.value.detail ==  "only admin can handel  this"


def test_delete_product_datas_check(mock_db):
    user =  fakeUser()
    admins = Fake_admin()
    data = products()

    p_id  = 1


    mock_db.query.return_value.filter.return_value.first.return_value = data


    result = delete_product_datas(p_id ,mock_db ,admins)

    result["message"] == "deleted successfully"


    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exec:
        delete_product_datas(p_id ,mock_db ,admins)


    assert exec.value.status_code == 404
    assert exec.value.detail == "Product not found"

    # non admins
    mock_db.query.return_value.filter.return_value.first.return_value = data


    with pytest.raises(HTTPException) as exec:
        delete_product_datas(p_id ,mock_db ,user)

    assert exec.value.status_code == 403
    assert exec.value.detail == "User not allow to delete product ,so only admn can handel this"


def test_get_product_details_check(mock_db):
    p_id = 1
    data = products()

    mock_db.query.return_value.filter.return_value.first.return_value = data

    result =  get_product_details(p_id , mock_db)

    assert result.name == "resberryphi"
    assert result.sku == "RES34"

    # no product
    
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exec:
        get_product_details(p_id , mock_db)

    assert exec.value.status_code == 404
    assert exec.value.detail == "no product available "


def test_get_all_product_details_check(mock_db):
    
    p_id = 1
    data = products()

    mock_db.query.return_value.all.return_value = data

    result =  get_all_product_details( mock_db)


    assert result.name == "resberryphi"
    assert result.sku == "RES34"

    mock_db.query.return_value.all.return_value = None

    with pytest.raises(HTTPException) as exec:
        get_all_product_details( mock_db)

    assert exec.value.status_code == 404
    assert exec.value.detail == "no product available "




