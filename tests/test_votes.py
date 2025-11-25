import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[2].id, user_id=test_user['id'])
    session.add(new_vote)


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post('/api/v1/vote/', json={'post_id': test_posts[0].id, 'dir': 1})

    assert res.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post('/api/v1/vote/', json={'post_id': test_posts[0].id, 'dir': 1})

    assert res.status_code == 201


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post('/api/v1/vote/', json={'post_id': test_posts[0].id, 'dir': 0})
    print('__res___', res)
    assert res.status_code == 201