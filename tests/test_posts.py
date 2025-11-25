import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/api/v1/posts/')

    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(posts_list) == len(test_posts)
    assert res.status_code == 200

def test_unauthorize_user_get_all_posts(client, test_posts):
    res = client.get('/api/v1/posts/')

    assert res.status_code == 401

def test_unauthorize_user_get_one_post(client, test_posts):
    res = client.get(f'/api/v1/posts/{test_posts[0].id}')

    assert res.status_code == 401

def test_get_one_post_not_exists(authorized_client):
    res = authorized_client.get(f'/api/v1/posts/{1233212}')

    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/api/v1/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize('title, content, published', [
    ("new title 1", "New title content 1", True),
    ("new title 2", "New title content 2", False),
    ("new title 3", "New title content 3", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(f'/api/v1/posts/', json={"title": title, "content": content, "published": published})
    
    create_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published
    assert create_post.owner_id == test_user['id']


def test_unauthorize_user_delete_post(client, test_user, test_posts):
    res = client.delete(f'/api/v1/posts/{test_posts[0].id}')

    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/api/v1/posts/{test_posts[0].id}')

    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/api/v1/posts/{2103192}')

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/api/v1/posts/{test_posts[2].id}')

    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title 1",
        "content": "Updated content 1",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f'/api/v1/posts/{test_posts[0].id}', json=data)
    updated_post = schemas.Post(**res.json()['data'])
    print(updated_post)

    assert res.status_code == 200
    assert updated_post.id == data['id']
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "Updated title 3",
        "content": "Updated content 3",
        "id": test_posts[2].id
    }

    res = authorized_client.put(f'/api/v1/posts/{test_posts[2].id}', json=data)

    assert res.status_code == 403

def test_unauthorize_user_update_post(client, test_user, test_posts):
    data = {
        "title": "Updated title 3",
        "content": "Updated content 3",
        "id": test_posts[2].id
    }

    res = client.put(f'/api/v1/posts/{test_posts[2].id}', json=data)

    assert res.status_code == 401

def test_update_post_not_exists(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title 3",
        "content": "Updated content 3",
        "id": test_posts[2].id
    }

    res = authorized_client.put(f'/api/v1/posts/{123}', json=data)

    assert res.status_code == 404