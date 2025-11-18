
from datetime import datetime
from types import SimpleNamespace
from app.main import app
from app.utils.auth import current_user
from app.models import Category

def test_create_category(client,fakeuser):
    app.dependency_overrides[current_user] = lambda :SimpleNamespace(**fakeuser)
    category={
    "name" : "electronics",
    "description" : "very nice",
    "is_active" : True,
    "created_at" : datetime.now().isoformat(),
    "updated_at" : datetime.now().isoformat()
    }
    response = client.post('category/create_category',json = category)
    assert response.status_code == 403
    data = response.json()
    assert data['detail'] == "You are not access to this only admins can handel the category"
    app.dependency_overrides.clear()

def test_create_category_validuser(client,Fake_admin):
    category={
    "name" : "electronics",
    "description" : "very nice",
    "is_active" : True,
    "created_at" : datetime.now().isoformat(),
    "updated_at" : datetime.now().isoformat()
    }
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)
    response = client.post('category/create_category',json=category)
    assert response.status_code == 200
    assert response.json()['message'] == "Category created successfully"


def test_update_categories(client,Fake_admin,db_session):
    
    # Override current_user to simulate admin access
    app.dependency_overrides[current_user] = lambda: SimpleNamespace(**Fake_admin)

    # Step 1: Create category
    category = {
        "name": "electronics",
        "description": "very nice",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    response = client.post('category/create_category', json=category)
    assert response.status_code == 200
    assert response.json()['message'] == "Category created successfully"

    # Step 2: Fetch created category from DB
    db_category = db_session.query(Category).filter(Category.name == "electronics").first()
    assert db_category is not None
    category_id = db_category.id

    # Step 3: Prepare updated data
    updated_category = {
        "name": "electronics",
        "description": "very nice project implemented using this",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    # Step 4: Update category
    response = client.put(f'category/update_category/{category_id}', json=updated_category)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "updated successfully"

    # Step 5: Verify updated record in DB
    updated = db_session.query(Category).filter(Category.id == category_id).first()
    assert updated.description == "very nice project implemented using this"

    app.dependency_overrides.clear()


def test_get_categories(client,Fake_admin,db_session):
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)
    category = {
        "name": "electronics",
        "description": "very nice",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    response = client.post('category/create_category', json=category)

    datas = db_session.query(Category).filter(Category.name == "electronics" ).first()
    category_id = datas.id
    assert category_id is not None
    response2 = client.get(f'category/get_category/{category_id}')
    assert response2.status_code == 200
   
    app.dependency_overrides.clear()



def test_delete_categories(client,db_session,fakeuser,Fake_admin):
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)
    category = {
        "name": "electronics",
        "description": "very nice",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    response = client.post('category/create_category', json=category)

    datas = db_session.query(Category).filter(Category.name == "electronics" ).first()
    category_id = datas.id
    assert category_id is not None

    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**fakeuser)
      
    
    response = client.delete(f'category/delete_category/{category_id}')
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not allowed to access this ,only admin can  delete"
    


# to delete successfully
    app.dependency_overrides[current_user] = lambda : SimpleNamespace(**Fake_admin)
   
  
    datas = db_session.query(Category).filter(Category.name == "electronics" ).first()
    category_id = datas.id
    assert category_id is not None

    response = client.delete(f'category/delete_category/{category_id}')
    assert response.status_code == 200 
    assert response.json()["message"] == "Category deleted successfully"

    response = client.delete(f'category/delete_category/9999')
    assert response.status_code == 404
    assert response.json()["detail"] == "No category available on thi s id "

    app.dependency_overrides.clear()
    
