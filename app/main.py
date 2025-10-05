from typing import Union, Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# -------------
# BASE MODEL
# ------------

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    

my_posts =[
    {
        "id": 1,
        "title": "Quantum Entanglement Explained",
        "content": "A detailed look into the bizarre connection between subatomic particles, even across vast distances.",
        "published": True,
        "rating": 4
    },
    {
        "id": 2,
        "title": "The History of AI",
        "content": "From Alan Turing to modern neural networks, tracing the evolution of artificial intelligence.",
        "published": True,
        "rating": 5
    },
    {
        "id": 3,
        "title": "Cooking Perfect Pasta",
        "content": "Tips and tricks for achieving 'al dente' perfection every time, focusing on technique and timing.",
        "published": False,
        "rating": None
    },
    {
        "id": 4,
        "title": "Deep Sea Exploration",
        "content": "Exploring the extreme environments and unique life forms found in the deepest parts of the ocean.",
        "published": True,
        "rating": 3
    },
    {
        "id": 5,
        "title": "Understanding the Stock Market",
        "content": "A beginner's guide to investments, trading, and common market terminology.",
        "published": False,
        "rating": 4
    }
]


# path operations
@app.get('/')
async def root():
    return {'message': 'Hello World Message Api'}


@app.get('/posts')
def get_posts():
    return {'data': my_posts}


# @app.post('/createposts')
# def create_posts(payload: dict=Body(...)):
#     print('----payload----', payload)
#     return {'new_post': f"title: {payload['title']} content: {payload['content']}"}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)

    print(post.rating)
    return {"data": post}


def find_post(id):
    for post in my_posts: 
        if post['id'] == id:
            return post

@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[int(len(my_posts)) - 1]
    return {"data": post}

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found!")

    return {"data": post}


def find_index_post(id):
    for idx, p in enumerate(my_posts):
        if p['id'] == id:
            return idx


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    # deleting post
    # remove item from the list
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found!")

    my_posts.pop(index)
    # return {'message': 'Post was successfully deleted.'}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'data': post_dict}