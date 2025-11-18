
from app.main import app
from app.utils.auth import current_user
from types import SimpleNamespace
def test_create_products(client,db_session,fakeuser,category_list,supplier_lists,Fake_admin,data):
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**fakeuser)
    category_id = category_list.id
    Supplier_id = supplier_lists.id
    response = client.post(f"/product/create_product/{category_id}/{Supplier_id}",json=data)

    assert response.status_code == 403

    assert response.json()["detail"] == "You are not allowed to create product detail table  only admins can handel it "

    
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)
    category_id = category_list.id
    Supplier_id = supplier_lists.id
    response = client.post(f"/product/create_product/{category_id}/{Supplier_id}",json = data)

    assert response.status_code == 200
    assert response.json()["message"] == "Your product details are enter successfully"


def test_Update_Products(client,data,products_list,db_session,Inventary_data,supplier_lists,category_list,fakeuser,Fake_admin):
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**fakeuser)
    product_id= products_list.id
    supplier_id=supplier_lists.id
    category_id = category_list.id

    response = client.put(f"/product/update_product/{product_id}/{supplier_id}/{category_id}",json = data)

    assert response.status_code == 403
    assert response.json()["detail"] == "only admin can handel  this"

    #  For real admin update tests
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)

    response = client.put(f"/product/update_product/{product_id}/{supplier_id}/{category_id}",json = data)

    assert response.status_code == 200
    assert response.json()["message"] == "Successfully updated"

    response = client.put(f"/product/update_product/{0}/{supplier_id}/{category_id}",json = data)
    assert response.status_code == 404
    assert response.json()["detail"] == "you entered wrong product which is not available"


def test_delete_product_datas(client,db_session,Inventary_data_for_delete,fakeuser,Fake_admin):
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**fakeuser)
    inventary,product = Inventary_data_for_delete
    p_id = product.id

    response = client.delete(f"/product/delete_product_data/{p_id}")

    assert response.status_code == 403
    assert response.json()["detail"] == "User not allow to delete product ,so only admn can handel this"
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)

    response = client.delete(f"/product/delete_product_data/{0}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
    
    response = client.delete(f"/product/delete_product_data/{p_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "deleted successfully"


def test_get_product_details(client,db_session,products_list):
    p_id = products_list.id
    response = client.get(f'/product/get_product_details/{0}')
    assert response.status_code == 404
    assert response.json()["detail"] ==  "no product available "
    response = client.get(f'/product/get_product_details/{p_id}')
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "kayboard"

def test_get_all_product_details(db_session,client,products_list):
    response = client.get('/product/get_all_product_details')
    assert response.status_code == 200

