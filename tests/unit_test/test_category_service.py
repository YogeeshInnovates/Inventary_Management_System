import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.services.category_service import Create_categories,update_categories ,get_categories,  delete_categories
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

class category:
    id = 1
    name = "electronics"
    description = "first item"
    is_active = "True"
    created_at = datetime.now()
    updated_at = datetime.now()

class Fake_admin:
    id = 1
    name = "Shiva"
    email ="Ram@gmail.com"
    password = "ram@1234"
    phone = 9354231414
    role = "admin"
    admin_code = "admin123"

def test_createa_category_check(mock_db):
    user = Fake_admin()
    categories = category()
    result = Create_categories(mock_db,categories,user)

    assert result["message"] == "Category created successfully"

    user_notadmin = fakeUser()
    with pytest.raises(HTTPException) as exec:
        Create_categories(mock_db,categories,user_notadmin)
    
    assert exec.value.status_code == 403
    assert exec.value.detail ==  "You are not access to this only admins can handel the category"


def test_update_category_check(mock_db):
    user = Fake_admin()
    categories = category()
    
    user_notadmin = fakeUser()

    mock_db.query.return_value.filter.return_value.first.return_value =  categories
    category_id = 1
    result = update_categories(category_id,categories,mock_db,user)
    assert result["message"] =="updated successfully"

    
    mock_db.query.return_value.filter.return_value.first.return_value =  None
    category_id = 1

    with pytest.raises(HTTPException) as exec:
        update_categories(category_id,categories,mock_db,user)

    assert exec.value.status_code == 404
    assert exec.value.detail ==  "No category present with this name"
    
    mock_db.query.return_value.filter.return_value.first.return_value =  categories

    with pytest.raises(HTTPException) as exec:
        update_categories(category_id,categories,mock_db,user_notadmin)

    assert exec.value.status_code == 403
    assert exec.value.detail == "You are not allow to access  ,only admin can modify the data"



def test_get_categories_check(mock_db):
    user = Fake_admin()
    categories = category()
    
    category_id = 1
    
    mock_db.query.return_value.filter.return_value.first.return_value = categories

    result  = get_categories(category_id ,mock_db ,user)
    assert result == categories

    
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exec:
        get_categories(category_id ,mock_db ,user)

    assert exec.value.status_code == 404
    assert exec.value.detail ==   "No category details available on this id"


def test_delete_categories_check(mock_db):
    user = Fake_admin()
    categories = category()
    category_id = 1
    
    user_notadmin = fakeUser()
    mock_db.query.return_value.filter.return_value.first.return_value =  categories

    result  =  delete_categories(category_id, mock_db ,user )

    assert result["message"] == "Category deleted successfully"

    # to check  no category present in db
    mock_db.query.return_value.filter.return_value.first.return_value =  None

    with pytest.raises(HTTPException) as exec:
        delete_categories(category_id, mock_db ,user )
    assert exec.value.status_code == 404
    assert exec.value.detail ==  "No category available on thi s id "

    # to check non admin user 

    mock_db.query.return_value.filter.return_value.first.return_value = categories

    with pytest.raises(HTTPException) as exec:
        delete_categories(category_id, mock_db ,user_notadmin )

    assert exec.value.status_code == 403
    assert exec.value.detail == "You are not allowed to access this ,only admin can  delete"



