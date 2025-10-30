from typing import Union, Optional, List
from fastapi import FastAPI, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# database models
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import utils
from .routes import post, user, auth


models.Base.metadata.create_all(bind=engine)

# __7.31.28

app = FastAPI()

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



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# path operations
@app.get('/')
async def root():
    return {'message': 'Hello World Message Api'}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {"data": posts}
