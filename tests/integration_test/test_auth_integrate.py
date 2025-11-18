
from app.services.auth_service import Signup,login_user

def test_Signup(client,fakeuser):
    response = client.post('/auth/signup',json = fakeuser)

    assert response.status_code == 200

    
    response = client.post('/auth/signup',json = fakeuser)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email already exists"


def test_signup_wrong_admin(client,Fake_admin_code):
    response = client.post('/auth/signup',json = Fake_admin_code)
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == "Invalid admin code"


def  test_login_user(client,fakeuser):

    response = client.post('/auth/signup',json = fakeuser)
    response2 = client.post('/auth/login',params={"email":fakeuser["email"],"password":"ram@1234"})

    assert response2.status_code == 200
    data = response2.json()
    assert data['message'] == "login successfully"


def test_login_nno_user(client,fakeuser):
    response = client.post('/auth/login',params={"email":fakeuser["email"],"password":"ram@1234"})
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == "User not found"

def test_login_wrong_passpwd(client,fakeuser):
    response = client.post('/auth/signup',json =fakeuser)
    response2 = client.post('/auth/login',params={"email":fakeuser["email"],"password":"abc123"})

    assert response2.status_code == 400

    data = response2.json()
    assert data["detail"] == "Invalid password"

# def login_user(db:Session,email:str,password:str,response):
#     db_user = db.query(User).filter(User.email == email).first()

#     if not db_user:
#         raise HTTPException(status_code = 404,detail="User not found")
    
#     if not pwd_context.verify(password,db_user.password):
#         raise HTTPException(status_code = 400,detail="Invalid password")

#     get_create_token = create_token({"sub": db_user.email}, timedelta(minutes=30))


#     response.set_cookie(
#     key="access_token",
#     value=get_create_token,
#     httponly=True,
#     max_age=12*3600
#         )

#     return {"message":"login successfully","token":get_create_token,"token_type":"bearer"}
