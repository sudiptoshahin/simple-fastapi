
from typing import Union, Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import utils, oauth2

router = APIRouter(
    prefix='/posts', # /post/{id}
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostResponse])
def get_posts(db: Session=Depends(get_db)):
    # raw SQL
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # ORM
    posts = db.query(models.Post).all()

    return posts


# @router.post('/createposts')
# def create_posts(payload: dict=Body(...)):
#     print('----payload----', payload)
#     return {'new_post': f"title: {payload['title']} content: {payload['content']}"}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    print('-----user_id--------', current_user)
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

    return new_post


@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id: str, response: Response, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # raw SQL
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found!")

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
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


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_post(id: str, updated_post: schemas.PostUpdate, db: Session=Depends(get_db)):

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