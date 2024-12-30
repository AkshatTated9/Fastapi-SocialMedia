from app import schema
import pytest
from jose import jwt
from app.config import settings 

def test_root(client):
    res = client.get('/')
    assert res.json()== "Homepage jai shree "

def test_usercreate(client):
    res =client.post("/user/",json={"email":"helo@gmail.com","password":"abcc"})
    new_user=schema.Returnuser(**res.json())
    print(res.json())
    assert new_user.email == "helo@gmail.com"
    assert res.status_code ==201

def test_login(client,test_user):
    user=client.post('/login',data={"username":test_user['email'],'password':test_user['password']})
    detail=user.json()
    payload = jwt.decode(detail['access_token'],settings.secret_key , algorithms=[settings.algorithm])
    id= payload.get("user_id")
    assert detail['token_type']=='bearer'
    assert test_user['id'] == id
    assert user.status_code == 200

@pytest.mark.parametrize("email,password,status_code",[('wrongemail.com','passweord',401),('asasas@gmail.com','abcc',401)])
def test_incorrectlogin(client,email,password,status_code):
    user=client.post('/login',data={"username":email,'password':password})
    assert status_code == 401
    assert user.json()['detail'] == 'Invalid Credentials'
