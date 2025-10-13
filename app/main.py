from typing import Union, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# database models
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

# database models

app = FastAPI()

# -------------

 5.30
# BASE MODEL
# ------------

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

# Database connection with psycopg2 adapter
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='simple-fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfull!')
        break
    except Exception as error:
        print(f"Connecting to database failed! \nError: {error}")
        time.sleep(2)
# End Database connection

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

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {"data": posts}

@app.get('/posts')
def get_posts(db: Session=Depends(get_db)):
    # raw SQL
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # ORM
    posts = db.query(models.Post).all()

    return {'data': posts}


# @app.post('/createposts')
# def create_posts(payload: dict=Body(...)):
#     print('----payload----', payload)
#     return {'new_post': f"title: {payload['title']} content: {payload['content']}"}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session=Depends(get_db)):
    print('-----create post--------', post)
    # raw SQL
    # cursor.execute(f"")
    # check SQL injection
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # ORM
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(post.model_dump())
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[int(len(my_posts)) - 1]
    return {"data": post}

@app.get('/posts/{id}')
def get_post(id: str, response: Response, db: Session=Depends(get_db)):
    
    # raw SQL
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

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
def delete_post(id: str, response: Response, db: Session=Depends(get_db)):

    # raw sql
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id, ))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found!")
    
    # ORM
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: str, updated_post: Post, db: Session=Depends(get_db)):

    # raw SQL
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s RETURNING * """, (post.title, post.content, post.published, id, ))
    # update_post = cursor.fetchone()
    # conn.commit()

    # ORM
    post_query = db.query(models.Post).filter(models.Post.id ==id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return {'data': post_query.first()}