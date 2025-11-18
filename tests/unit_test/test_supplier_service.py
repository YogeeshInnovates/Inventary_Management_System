from fastapi import HTTPException
from unittest.mock import MagicMock
from datetime import datetime
import pytest
from app.services.supplier_service import create_supplieries,update_supplieries,delete_supplieries ,supplier_details

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

class Supplier:
    id =1
    name= "Satish"
    contact_person = 9352426249
    email = "supplier@gmail.com"
    address = "first phase"
    city = "Bangalore"
    state = "Karnataka"
    country = "India"
    notes = "notes available here"
    is_active = "True"
    created_at = datetime.now()
    updated_at = datetime.now()

class updated_Supplier:
    id =1
    name= "Harish"
    contact_person = 9352426249
    email = "supplier@gmail.com"
    address = "first phase"
    city = "Bangalore"
    state = "Karnataka"
    country = "India"
    notes = "notes available here2"
    is_active = "True"
    created_at = datetime.now()
    updated_at = datetime.now()

def test_create_supplier_check(mock_db):
    supplier = Supplier()
    admin = Fake_admin()
    user = fakeUser()


    result = create_supplieries(supplier,mock_db,admin)

    assert result["message"] == "supplier entries done succcessfully"

    with pytest.raises(HTTPException) as exec:
        create_supplieries(supplier,mock_db,user)
    
    assert exec.value.status_code == 403
    assert exec.value.detail == "You are not allowed to access for this id only admin can  insert details"
        
def test_update_supplieries_check(mock_db):
    supplier = Supplier()
    admin = Fake_admin()
    user = fakeUser()
    update_sales = updated_Supplier()
    supplier_id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = supplier


    result = update_supplieries(supplier_id, update_sales ,mock_db ,admin)

    updated = mock_db.query.return_value.filter.return_value.first.return_value

    assert updated.name =="Harish"
    assert updated.notes == "notes available here2"

    assert result["message"] == "Supplier details  updated successfully"

    # non admin check

    with pytest.raises(HTTPException) as exec:
        update_supplieries(supplier_id, update_sales ,mock_db ,user)
    assert exec.value.status_code == 403
    assert exec.value.detail == "You are not allowed to update this only admin can update"

    #None return check 
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exec:
        update_supplieries(supplier_id, update_sales ,mock_db ,admin)
    assert exec.value.status_code == 404
    assert exec.value.detail =="NO supplier available on this id"

def test_delete_supplieries_check(mock_db):
    supplier = Supplier()
    admin = Fake_admin()
    user = fakeUser()
    update_sales = updated_Supplier()
    supplier_id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = supplier

    result = delete_supplieries(supplier_id , mock_db ,admin)

    assert result["message"] == "supplier deleted successfully"

    # non admin

    with pytest.raises(HTTPException) as exec:
        delete_supplieries(supplier_id , mock_db ,user)

    assert exec.value.status_code == 403
    assert exec.value.detail == "You are not able to dlete this only admin can delete"

def test_supplier_details_check(mock_db):
    supplier = Supplier()
    user = fakeUser()
    supplier_id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = supplier

    result = supplier_details(supplier_id ,mock_db ,user)

    assert result.name ==  "Satish"
    
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exec:
        supplier_details(supplier_id ,mock_db ,user)
    
    assert exec.value.status_code == 404
    assert exec.value.detail ==  "No supplier info  available here"

# def supplier_details(supplier_id ,db ,user):
#     db_supplier_data=db.query(Supplier).filter(Supplier.id == supplier_id).first()

#     if db_supplier_data is None:
#         raise HTTPException(status_cide = 404 , detail = "No supplier info  available here")
    
#     return db_supplier_data

