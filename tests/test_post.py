from app import schema
import pytest
def test_getallpost(client,test_posts):
    res=client.get('/posts/')
    def validate(post):
        return schema.Postout(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code==200

def test_particularpost(test_posts, client):
    res = client.get(f'/posts/{test_posts[0].id}')
    print(res.json())

    # Extract nested data from the response JSON to match the schema
    response_data = res.json()
    post_data = response_data.get("Post", {})
    
    post = schema.Returnpost(**post_data)
    
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content
    assert post.title == test_posts[0].title
    

def test_incorrexrpostid(client):
    res = client.get('/posts/888')
    print(res.json())
    assert res.status_code == 404

    
@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authoriseduser, test_user, title, content, published):
    res = authoriseduser.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schema.Returnpost(**res.json())
    assert res.status_code == 200
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_authoriseduser_createpost(client, test_user, title, content, published):
    res = client.post(
        "/posts/", json={"title": title, "content": content, "published": published})
    assert res.status_code == 401

def test_deletepost(authoriseduser,test_posts):
    res=authoriseduser.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code==200

def test_delete_unavailablepost(authoriseduser):
    res=authoriseduser.delete(f"/posts/888")
    assert res.status_code==404

def test_delete_unauthuser(authoriseduser,test_posts):
    res=authoriseduser.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code==403

def test_update_post(authoriseduser, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authoriseduser.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authoriseduser, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authoriseduser.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403
