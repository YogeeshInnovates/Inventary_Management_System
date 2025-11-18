from app.main  import app
from app.models import Inventary_products,User_Pick_object
from app.utils.auth import current_user
from types import SimpleNamespace

def test_User_Picking_Datas(client,db_session, user, Users_Pick,User_Pick_objects,Inventary_data):
    data =  Users_Pick
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**user)
    product_id = Inventary_data.product_id

    response = client.post(f'/User_activity/User_Picking_Data/{product_id}',json = data)

    assert response.status_code == 200
    assert response.json()["message"] == "successfully taken by user"


def test_User_Picking_Datas_wrongdata(client,db_session, user, Users_Pick,User_Pick_objects,Inventary_data):
    data =  Users_Pick
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**user)
    product_id = Inventary_data.product_id
    data_inventary = db_session.query(Inventary_products).filter(Inventary_products.product_id == product_id).first()
    data_inventary.quantity_in_stock = 0
    db_session.add(data_inventary)
    db_session.commit()
    db_session.refresh(data_inventary)
    response = client.post(f'/User_activity/User_Picking_Data/{product_id}',json = data)

    assert response.status_code == 404
    assert response.json()["detail"] == "No product available"

    data_inventary.quantity_in_stock = 5
    db_session.add(data_inventary)
    db_session.commit()
    db_session.refresh(data_inventary)

    val = data.copy()
    val["quantity_of_taking_product"]=20

    response = client.post(f'/User_activity/User_Picking_Data/{product_id}',json = val)

    assert response.status_code == 409
    assert response.json()["detail"] == "No that much product available"


    data_inventary.quantity_in_stock =10
    data_inventary.quantity_taken_byuser =5
    db_session.add(data_inventary)
    db_session.commit()
    db_session.refresh(data_inventary)
    val["quantity_of_taking_product"]=8

    response = client.post(f'/User_activity/User_Picking_Data/{product_id}',json = val)

    assert response.status_code == 409
    assert response.json()["detail"] == "User not able to get that much bacuse already taken by other user"



def test_User_return_Datas(client,db_session,products_list, user,User_Pick_objects,Inventary_data):

    
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**user)
    product_id = Inventary_data.product_id
    quantity_of_return_product = 1
    status_usage = "returned"
    response = client.post(f'/User_activity/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}')

    assert response.status_code == 200
    
    response.json()["message"] == "Successfully returned or updation done,Thank you "

    product_id = Inventary_data.product_id
    quantity_of_return_product = 30
    status_usage = "returned"
    response = client.post(f'/User_activity/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}')

    assert response.status_code == 400
    assert response.json()["detail"] == "Return quantity exceeds picked quantity"

    product_id = Inventary_data.product_id
    quantity_of_return_product = 2
    status_usage = "returned"
    response = client.post(f'/User_activity/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}')
    assert response.status_code == 200
    
    response.json()["message"] == "Successfully returned or updation done,Thank you "
    data_inventary = db_session.query(User_Pick_object).filter(User_Pick_object.product_id == product_id).first()
    assert data_inventary.quantity_of_taking_product == 0

    product_id = Inventary_data.product_id+1
    quantity_of_return_product = 2
    status_usage = "returned"
    response = client.post(f'/User_activity/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}')
    assert response.status_code == 404
    assert response.json()["detail"] == "This user have not taken anything"



def test_User_return_Datas_used(client,db_session,products_list, user,User_Pick_objects,Inventary_data):
    
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**user)
    product_id = Inventary_data.product_id
    quantity_of_return_product = 1
    status_usage = "used"
    response = client.post(f'/User_activity/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}')

    assert response.status_code == 200
    
    response.json()["message"] == "Successfully returned or updation done,Thank you "

    product_id = Inventary_data.product_id
    quantity_of_return_product = 30
    status_usage = "used"
    response = client.post(f'/User_activity/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}')

    assert response.status_code == 400
    assert response.json()["detail"] == "Return quantity exceeds picked quantity"

    product_id = Inventary_data.product_id
    quantity_of_return_product = 2
    status_usage = "used"
    response = client.post(f'/User_activity/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}')
    assert response.status_code == 200
    
    response.json()["message"] == "Successfully returned or updation done,Thank you "
    data_inventary = db_session.query(User_Pick_object).filter(User_Pick_object.product_id == product_id).first()
    assert data_inventary.quantity_of_taking_product == 0

    product_id = Inventary_data.product_id+1
    quantity_of_return_product = 2
    status_usage = "used"
    response = client.post(f'/User_activity/User_return_Data/{product_id}/{quantity_of_return_product}/{status_usage}')
    assert response.status_code == 404
    assert response.json()["detail"] == "This user have not taken anything"

    
    product_id = Inventary_data.product_id
    Inventary_product_datas = db_session.query(Inventary_products).filter(Inventary_products.product_id == product_id).first()
    assert Inventary_product_datas.quantity_taken_byuser ==0
    assert Inventary_product_datas.quantity_in_stock == 7

def test_getProductcarryUser_details(client,products_list,user,db_session,Users,User_Pick_objects,Inventary_data):
    
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**user)
    response = client.get('/User_activity/getProductcarryUser_details')
    assert response.status_code == 200
    assert response.json() is not None

