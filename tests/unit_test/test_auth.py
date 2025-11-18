
from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from app.services.auth_service import Signup, login_user
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

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
class fakeUser_login:
    id = 1
    name = "Ram"
    email ="Ram@gmail.com"
    password = pwd_context.hash("ram@1234")
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

class Fake_admin_code:
    id = 1
    name = "Shiva"
    email ="Ram@gmail.com"
    password = pwd_context.hash("ram@1234")
    password = "ram@1234"
    phone = 9354231414
    role = "admin"
    admin_code = "12admin123"


def test_signup_success(mock_db):
    user=fakeUser()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = Signup(user, mock_db)

    assert result.name == "Ram"
    assert result.email == "Ram@gmail.com"

    mock_db.add.assert_called_once_with(result)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(result)

def test_fail_signup(mock_db):
    user=fakeUser()

    mock_db.query.return_value.filter.return_value.first.return_value = user

    with pytest.raises(HTTPException) as exec:
        Signup(user, mock_db)

    assert exec.value.status_code == 400
    assert exec.value.detail == "Email already exists"

def test_admin_auth(mock_db):
    user=Fake_admin()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = Signup(user, mock_db)

    assert result.name == "Shiva"
    assert result.email == "Ram@gmail.com"

    mock_db.add.assert_called_once_with(result)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(result)

    
def test_wrong_admin_code(mock_db):
    user= Fake_admin_code()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises (HTTPException) as exec:
        Signup(user, mock_db)
    
    assert exec.value.status_code ==  400 
    assert exec.value.detail ==  "Invalid admin code"


def test_login_success(mock_db):
    user = fakeUser_login()

    email ="Ram@gmail.com"
    password ="ram@1234"
    response = MagicMock()
    
    mock_db.query.return_value.filter.return_value.first.return_value = user

    result  = login_user(mock_db,email,password,response)

    assert result["message"] == "login successfully"

def test_login_no_userfound(mock_db):
    user =  fakeUser_login()

    email ="Ram23@gmail.com"
    password ="ram@1234"

    mock_db.query.return_value.filter.return_value.first.return_value = None
    response = MagicMock()
    with pytest.raises (HTTPException) as exec:
        login_user(mock_db,email,password,response)

    assert exec.value.status_code == 404
    assert exec.value.detail == "User not found"

    email ="Ram@gmail.com"
    password ="ram@123478"
    
    mock_db.query.return_value.filter.return_value.first.return_value = user

    with pytest.raises(HTTPException) as exec:
        login_user(mock_db,email,password,response)
    
    assert exec.value.status_code == 400
    assert exec.value.detail == "Invalid password"

