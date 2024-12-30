from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db,Base
from app import models
from alembic import command
import pytest
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import create_engine
from app.oauth2 import accesstokencreate


#Creating a testing database so that original db remains unaltered
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/Test_Database'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
Testingsessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture
def session():

    #command.downgrade("base")                       #if using alembic
    models.Base.metadata.drop_all(bind=engine)
    # command.upgrade("head")                       #if using alembic
    models.Base.metadata.create_all(bind=engine)
    db=Testingsessionlocal()
    try:
        yield db
    finally:
        db.close()

# Creating test client obj and performing tests
@pytest.fixture
def client(session):
    def override_get_db():
        db=Testingsessionlocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user={"email":"ram@gmail.com","password":"abcc"}
    tetuser=client.post("/user/",json=user)
    assert tetuser.status_code == 201
    new_user=tetuser.json()
    new_user['password']=user["password"]
    return new_user

@pytest.fixture
def test_user1(client):
    user={"email":"raam@gmail.com","password":"abcc"}
    tetuser=client.post("/user/",json=user)
    assert tetuser.status_code == 201
    new_user=tetuser.json()
    new_user['password']=user["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return accesstokencreate({"user_id":test_user['id']})

@pytest.fixture
def authoriseduser(client,token):
    client.headers ={
        **client.headers,
        "Authorization":f'Bearer {token}'
    }
    return client
@pytest.fixture
def test_posts(test_user, session,test_user1):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user1['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts