
from typing import Union, Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import utils, oauth2
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix='/posts', # /post/{id}
    tags=['Posts']
)

# @router.get('/', response_model=List[schemas.PostResponse])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db), current_user: str=Depends(oauth2.get_current_user), limit: int=30, skip: int=0, search: Optional[str]=""):
    # raw SQL
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # ORM
    try:
        posts = (
            db.query(models.Post)
            .filter(models.Post.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )

        results = db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, 
            models.Vote.post_id == models.Post.id,
            isouter=True
        ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        # print('___results____', results)
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        posts = []

    return results


# @router.post('/createposts')
# def create_posts(payload: dict=Body(...)):
#     print('----payload----', payload)
#     return {'new_post': f"title: {payload['title']} content: {payload['content']}"}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: str=Depends(oauth2.get_current_user)):
    # raw SQL
    # cursor.execute(f"")
    # check SQL injection
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # ORM
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(post.model_dump())

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: str, response: Response, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # raw SQL
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    # post = cursor.fetchone()

    # post_query = db.query(models.Post).filter(models.Post.id == id)
    post_query = db.query(
        models.Post,
        func.count(models.Vote.post_id).label('votes')
    ).join(
        models.Vote, 
        models.Vote.post_id == models.Post.id, 
        isouter=True
    ).group_by(
        models.Post
    ).filter(
        models.Post.id == id
    )

    post = post_query.first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found!")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=f"Not authorized to perform this action."
    #     )

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str, response: Response, db: Session=Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    # raw sql
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id, ))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found!")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform this action."
        )
    
    # ORM
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_post(id: str, updated_post: schemas.PostUpdate, db: Session=Depends(get_db), current_user: str=Depends(oauth2.get_current_user)):

    # raw SQL
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s RETURNING * """, (post.title, post.content, post.published, id, ))
    # update_post = cursor.fetchone()
    # conn.commit()

    # ORM
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform this action."
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return {'data': post_query.first()}