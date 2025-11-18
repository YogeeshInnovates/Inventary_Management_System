from app.main import app
from app.utils.auth import current_user
from types import SimpleNamespace
def test_create_supplieries(client,db_session,SupplierData,fakeuser,Fake_admin):
    supplier = SupplierData
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**fakeuser)

    response = client.post("/suppler_details/create_supplier",json = supplier)
    print("This is response",response.json())

    assert response.status_code == 403
    assert response.json()["detail"] == "You are not allowed to access for this id only admin can  insert details"

    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)

    response = client.post("/suppler_details/create_supplier",json = supplier)

    assert response.status_code  == 200
    assert response.json()["message"] == "supplier entries done succcessfully"


def test_update_supplieries(client,db_session,SupplierData,supplier_lists,fakeuser,Fake_admin):
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**fakeuser)
    supplier = SupplierData

    supplier_id = supplier_lists.id

    response = client.put(f"/suppler_details/update_supplier/{supplier_id}",json = supplier)
    assert response.status_code == 403 
    assert response.json()["detail"] ==  "You are not allowed to update this only admin can update"
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)

    response = client.put(f"/suppler_details/update_supplier/{supplier_id}",json = supplier)
    assert response.status_code == 200
    assert response.json()["message"] == "Supplier details  updated successfully"

    supplier_id =0 

    response = client.put(f"/suppler_details/update_supplier/{supplier_id}",json = supplier)
    assert response.status_code == 404
    assert response.json()["detail"] == "NO supplier available on this id"

def test_delete_supplieries(db_session,client,fakeuser,Fake_admin,supplier_lists):
    app.dependency_overrides[current_user] = lambda:SimpleNamespace(**fakeuser)
    supplier_id = supplier_lists.id

    response = client.delete(f'/suppler_details/delete_supplier/{supplier_id}')

    assert response.status_code == 403
    assert response.json()["detail"] == "You are not able to dlete this only admin can delete"

    app.dependency_overrides[current_user] = lambda:SimpleNamespace(**Fake_admin)

    
    response = client.delete(f'/suppler_details/delete_supplier/{supplier_id}')

    assert response.status_code == 200
    assert response.json()["message"] == "supplier deleted successfully"


def test_supplier_details(db_session,client,supplier_lists,fakeuser):
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**fakeuser)
    supplier_id = 0

    response = client.get(f'/suppler_details/supplier_details/{supplier_id}')

    assert response.status_code == 404
    assert response.json()["detail"] == "No supplier info  available here"

    
    supplier_id = supplier_lists.id
    response = client.get(f'/suppler_details/supplier_details/{supplier_id}')

    assert response.status_code == 200
    assert response.json()["address"] == 'bangalore electronics city'


