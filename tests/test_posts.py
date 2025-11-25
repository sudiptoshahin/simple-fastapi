import pytest

def test_get_all_posts(authorized_client, test_user):
    res = authorized_client.get('/api/v1/posts/')
    print(res.json())
    assert res.status_code == 200