from app.main import app
from types import SimpleNamespace
from app.utils.auth import current_user

def test_create_sales_records(db_session,products_list,client,sales_data,fakeuser,Fake_admin):
    data = sales_data
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**fakeuser)
    product_id = products_list.id

    response = client.post(f'/sales/create_sales_record/{product_id}',json = data)

    assert response.status_code == 403
    
    assert response.json()["detail"] ==  "Only admin can handel this "

    
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)
    
    response = client.post(f'/sales/create_sales_record/{product_id}',json = data)

    assert response.status_code == 200
    assert response.json()["message"] == "Create sales record successfully"


def test_update_sales_records(client,db_session,sales_data,sales_data_stored,fakeuser,Fake_admin):
    app.dependency_overrides[current_user] = lambda :SimpleNamespace(**fakeuser)
    data = sales_data
    product_id = sales_data_stored.product_id

    response = client.put(f"sales/update_sales_record/{product_id}",json = data)

    assert response.status_code == 403
    assert response.json()["detail"] == "Only admin can hndel sales data"

    app.dependency_overrides[current_user] = lambda: SimpleNamespace(**Fake_admin)

    response = client.put(f"sales/update_sales_record/{product_id}",json = data)
    assert response.status_code == 200
    assert response.json()["message"] == "Update sales record successfully"

    product_id =1000
    response = client.put(f"sales/update_sales_record/{product_id}",json = data)
    assert response.status_code == 404
    assert response.json()["detail"] == "No saels record on this product"


def test_view_all_sales_datas(client,db_session,sales_data_stored):
    response = client.get('sales/view_all_sales_data')

    assert response.status_code == 200
    assert response.json()[0]["customer_name"] == "Gopal"


def test_delete_sales_datas(client,db_session,fakeuser,Fake_admin,sales_data_stored):
    app.dependency_overrides[current_user] = lambda: SimpleNamespace(**fakeuser)
    sales_id = sales_data_stored.id
    response = client.delete(f'sales/delete_sales_data/{sales_id}')

    assert response.status_code == 403
    assert response.json()["detail"] == "only admin can delete sales data"

    app.dependency_overrides[current_user] = lambda: SimpleNamespace(**Fake_admin)

    response = client.delete(f'sales/delete_sales_data/{sales_id}')

    assert response.status_code == 200
    assert response.json()["message"] == "deleted successfully"
