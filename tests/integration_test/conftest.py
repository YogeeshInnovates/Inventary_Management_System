import pytest
from sqlalchemy import create_engine
from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient
from app.database import Base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from app.models import User,Inventary_products,Products, Category,Supplier,Sales,User_Pick_object
from datetime import datetime

POSTGRE_URL = 'postgresql://postgres:password@localhost/inventary_test'

engine = create_engine(POSTGRE_URL)
SessionMaker = sessionmaker(autocommit = False,autoflush=False,bind = engine)
Base.metadata.create_all(bind = engine)

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")
@pytest.fixture
def db_session():
    connection = engine.connect()
    transection = connection.begin()
    db = SessionMaker(bind = connection)

    try:
        yield db
    finally:
        db.close()
        transection.rollback()
        connection.close()
        


@pytest.fixture
def category_list(db_session):
    category = Category(
    name = "electronics",
    description = "electronics items",
    is_active = True,
    created_at = datetime.now().isoformat(),
    updated_at = datetime.now().isoformat()
    )

    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def supplier_lists(db_session):
    supplier = Supplier(
   
    name= "Rkesh",
    contact_person = "4858943339",
    email = "supplier@gmail.com",
    address = "bangalore electronics city",
    city = "electronics city",
    state ="Karnataka",
    country = "India",
    notes = "Very good products",
    is_active = True,
    created_at = datetime.now().isoformat(),

    updated_at = datetime.now().isoformat()

    )

    db_session.add(supplier)
    db_session.commit()
    return supplier

@pytest.fixture
def products_list(db_session,category_list,supplier_lists):
    products = Products(
    name = "kayboard",
    category_id =category_list.id,
    Supplier_id = supplier_lists.id,
    sku = "KEY-101",
    price = 8000,
    quantity_in_stock =10,
    reorder_level =1,
    description = "very nice performance",
    is_active = True,
    created_at = datetime.now().isoformat(),
    updated_at = datetime.now().isoformat()

     )

    db_session.add(products )
    db_session.commit()
    return products

@pytest.fixture
def Inventary_data(db_session,products_list,category_list,supplier_lists):
    item1 = Inventary_products(
    product_id  =products_list.id ,
    name = "keyboard",
    sku = "KEY-101",
    quantity_in_stock =  10,
    quantity_taken_byuser=3
    )
   
    db_session.add(item1)
    db_session.commit()

    return item1


      
@pytest.fixture
def Inventary_data_for_delete(db_session):
    category = Category(
    name = "electronics",
    description = "electronics items",
    is_active = True,
    created_at = datetime.now().isoformat(),
    updated_at = datetime.now().isoformat()
    )

    db_session.add(category)
    db_session.commit()
    supplier = Supplier(
   
    name= "Rkesh",
    contact_person = "4858943339",
    email = "supplier@gmail.com",
    address = "bangalore electronics city",
    city = "electronics city",
    state ="Karnataka",
    country = "India",
    notes = "Very good products",
    is_active = True,
    created_at = datetime.now().isoformat(),

    updated_at = datetime.now().isoformat()

    )

    db_session.add(supplier)
    db_session.commit()

    products = Products(
    name = "kayboard",
    category_id = category.id,
    Supplier_id = supplier.id,
    sku = "KEY-101",
    price = 8000,
    quantity_in_stock =10,
    reorder_level =1,
    description = "very nice performance",
    is_active = True,
    created_at = datetime.now().isoformat(),
    updated_at = datetime.now().isoformat()

     )

    db_session.add(products )
    db_session.commit()

    item1 = Inventary_products(
    product_id  =products.id ,
    name = "keyboard",
    sku = "KEY-101",
    quantity_in_stock =  10,
    quantity_taken_byuser=2
    )
   
    db_session.add(item1)
    db_session.commit()

    return item1,products


@pytest.fixture
def  Users(db_session):
    user = User(
    updated_at = datetime.now().isoformat(),

    name = "Ram",
    email = "example@gmail.com",
    password = pwd_context.hash("ram@1234"),
    phone = "4358947895",
    role = "user",
    )

    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = lambda : db_session 

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def user(Users):
    return{
    "id":Users.id
    }

@pytest.fixture
def fakeuser():
    return{
    "id" : 1,
    "name" : "Ram",
    "email" : "Ram@gmail.com",
    "password"  : "ram@1234",
    "phone" : 9354231414,
    "role" : "user"
    }


@pytest.fixture
def fakeuser2user():
    return User(
        id=1,
        name="Ram",
        email="Ram@gmail.com",
        password="ram@1234",
        phone="9354231414",
        role="user"
    )


@pytest.fixture
def fakeuser2admin():
    return User(
        id=1,
        name="Ram",
        email="Ram@gmail.com",
        password="ram@1234",
        phone="9354231414",
        role="user"
    )

@pytest.fixture
def fakeUser_login():
    return{
    "id" : 1,
    "name" : "Ram",
    "email" : "Ram@gmail.com",
    "password" : "abcd123",
    "phone" : 9354231414,
    "role" : "user"

    }

@pytest.fixture
def Fake_admin():
    return{
    "id" : 1,
   "name": "Shiva",
    "email" :"Ram@gmail.com",
    "password" : "ram@1234",
    "phone" : 9354231414,
    "role" : "admin",
    "admin_code" : "admin123"
    }

@pytest.fixture
def  Fake_admin_code():
    return{
    "id" : 1,
    "name" : "Shiva",
    "email" :"Ram@gmail.com",
    "password" : pwd_context.hash("ram@1234"),
    "password" : "ram@1234",
    "phone" : 9354231414,
    "role" : "admin",
    "admin_code" : "12admin123",
    }

@pytest.fixture
def data(supplier_lists,category_list):
    return{
    "name": "Keyboard",
    "category_id": category_list.id,
    "Supplier_id": supplier_lists.id,
    "sku": "KEY_101",
    "price": 8000,
    "quantity_in_stock": 10,
    "reorder_level":1,
    "description":"products keyboard hign efficiency keyboard",
    "is_active":  True,
    "created_at": datetime.now().isoformat(),
    "updated_at": datetime.now().isoformat()
    }


@pytest.fixture
def sales_data(products_list):
    return{
    "quantity": 3,
    "sale_date": datetime.now().isoformat(),
    "customer_name": "Ramesh",
    "total_revenue": 10000
    }



@pytest.fixture
def sales_data_stored(db_session,products_list):
    sales = Sales(
    product_id = products_list.id,
    quantity = 10,
    sale_price = 10000,
    sale_date = datetime.now().isoformat(),
    customer_name = "Gopal"
    )
    db_session.add(sales)
    db_session.commit()
    return sales


@pytest.fixture
def SupplierData():
    return{
    "name": "Ram",
    "contact_person":"3897437896",
    "email": "example@gmail.com",
    "address": "bangalore",
    "city": "electronic city",
    "state": "Karnataka",
    "country": "India",
    "notes": "New sales record",
    "is_active": True,
    "created_at": datetime.now().isoformat(),
    "updated_at":datetime.now().isoformat()
    }

@pytest.fixture
def  Users_Pick(products_list):
    return{
    "Name_of_object_taker": "Ramesh",
    "product_id" : products_list.id,
    "quantity_of_taking_product" : 3,
    "picking_date" :  datetime.now().isoformat(),
   
    "status_of_getting"  : "Not return",
    "return_date_time" : datetime.now().isoformat()
    }


@pytest.fixture
def  User_Pick_objects(db_session,products_list,Users):
    user_pick = User_Pick_object(
    Name_of_object_taker = "Ramesh",
    product_id = products_list.id,
    quantity_of_taking_product = 3,
    picking_date = datetime.now().isoformat(),
    user_id = Users.id,
    status_of_getting =  True,
    return_date_time =datetime.now().isoformat()
    )
    db_session.add(user_pick)
    db_session.commit()