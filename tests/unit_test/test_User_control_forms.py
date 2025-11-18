from fastapi import HTTPException
import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.services.user_control_forms_service import User_Picking_Datas,User_return_Datas,getProductcarryUser_details
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
class Inventary:
    id = 1
    product_id = 1
    name = "resberryphi"
    sku ="RES34"
    quantity_in_stock = 10
    quantity_taken_byuser= 8

      
class Empty_Inventary:
    id = 1
    product_id = 1
    name = "resberryphi"
    sku ="RES34"
    quantity_in_stock = 0
    quantity_taken_byuser= 0

class User_pick:
    
    Name_of_object_taker = "Harish"
    product_id = 1
    quantity_of_taking_product = 10
    picking_date = datetime.now()
   
    status_of_getting  = "Not return"
    return_date_time = datetime.now()

class success_User_pick:
    
    Name_of_object_taker = "Harish"
    product_id = 1
    quantity_of_taking_product = 1
    picking_date = datetime.now()
   
    status_of_getting  = "Not return"
    return_date_time = datetime.now()

class User_pick_highpick:
    
    Name_of_object_taker = "Harish"
    product_id = 1
    quantity_of_taking_product = 21
    picking_date = datetime.now()
   
    status_of_getting  = "Not return"
    return_date_time = datetime.now()

def test_User_Picking_Datas_check(mock_db):
     user = fakeUser()
     data = User_pick()
     highpick= User_pick_highpick()
     success_data = success_User_pick()
     product_id = 1
    
     empty_product = Empty_Inventary()
     products = Inventary()

     mock_db.query.return_value.filter.return_value.first.return_value = empty_product

     with pytest.raises(HTTPException) as exec:
        User_Picking_Datas(product_id ,data ,mock_db ,user)
     assert exec.value.status_code == 404
     assert exec.value.detail == "No product available"


     mock_db.query.return_value.filter.return_value.first.return_value = products

     with pytest.raises(HTTPException) as exec:
        User_Picking_Datas(product_id ,highpick ,mock_db ,user)
     assert exec.value.status_code == 409
     assert exec.value.detail == "No that much product available"


     with pytest.raises(HTTPException) as exec:
        User_Picking_Datas(product_id ,data ,mock_db ,user)
     assert exec.value.status_code == 409
     assert exec.value.detail == "User not able to get that much bacuse already taken by other user"


     mock_db.query.return_value.filter.return_value.first.side_effect = [products, None]

     result = User_Picking_Datas(product_id, success_data, mock_db, user)

     assert result["message"] == "successfully taken by user"
                                 

def test_User_return_Datas_all_cases(mock_db):
    user = fakeUser()

    
    # Case 1: User has not taken any product -> HTTP 404
   
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc1:
        User_return_Datas(product_id=1, quantity_of_return_product=2, status_usage="returned", db=mock_db, user=user)
    assert exc1.value.status_code == 404
    assert exc1.value.detail == "This user have not taken anything"

    pick = User_pick() 
    inv = Inventary()   # quantity_taken_byuser = 8, quantity_in_stock = 10
    mock_db.query.return_value.filter.return_value.first.side_effect = [pick, inv]

    with pytest.raises(HTTPException) as exc2:
        User_return_Datas(product_id=1, quantity_of_return_product=15, status_usage="returned", db=mock_db, user=user)
    assert exc2.value.status_code == 400
    assert exc2.value.detail == "Return quantity exceeds picked quantity"

    
    # Successful return with status = "returned"

    pick = User_pick()  # quantity_of_taking_product = 10
    inv = Inventary()   # quantity_taken_byuser = 8, quantity_in_stock = 10
    mock_db.query.return_value.filter.return_value.first.side_effect = [pick, inv]

    result_returned = User_return_Datas(product_id=1, quantity_of_return_product=3, status_usage="returned", db=mock_db, user=user)
    assert result_returned["message"] == "Successfully returned or updation done,Thank you "
    assert pick.quantity_of_taking_product == 7  # 10 - 3
    assert inv.quantity_taken_byuser == 5        # 8 - 3

    
    # Successful return with status = "used"

    pick = User_pick()  # quantity_of_taking_product = 10
    inv = Inventary()   # quantity_taken_byuser = 8, quantity_in_stock = 10
    mock_db.query.return_value.filter.return_value.first.side_effect = [pick, inv]

    result_used = User_return_Datas(product_id=1, quantity_of_return_product=3, status_usage="used", db=mock_db, user=user)
    assert result_used["message"] == "Successfully returned or updation done,Thank you "
    assert pick.quantity_of_taking_product == 7       # 10 - 3
    assert inv.quantity_taken_byuser == 5            # 8 - 3
    assert inv.quantity_in_stock == 7                # 10 - 3 because 'used


def test_getProductcarryUser_details(mock_db):

    mock_user1 = MagicMock()
    mock_user1.id = 1
    mock_user1.name = "Ram"
    mock_user1.pick_object = [success_User_pick]

    mock_user2 = MagicMock()
    mock_user2.id = 2
    mock_user2.name = "Shiva"
    mock_user2.pick_object = []  # No picks

    # Mock DB query for users
    mock_db.query.return_value.join.return_value.all.return_value = [mock_user1, mock_user2]

    # Mock DB query for products
    mock_product = Inventary()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_product

    # Call the function
    from app.services.user_control_forms_service import getProductcarryUser_details
    result = getProductcarryUser_details(mock_db)

    assert len(result) == 2
    assert result[0]["user_name"] == "Ram"
    assert len(result[0]["product_taken"]) == 1
    assert result[0]["product_taken"][0]["product_name"] == mock_product.name
    assert result[1]["product_taken"] == []  # no picks for second user
