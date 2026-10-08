from app import oauth2

from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException,Response,status,Depends,APIRouter
from typing import List

router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session= Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts""")
    # posts=cur.fetchall()
    # return {"message": posts}
    posts=db.query(models.Post).all()
    return  posts



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def creates_post(post: schemas.PostBase ,db: Session=Depends(get_db),current_user:models.User =Depends(oauth2.get_current_user)): 
    # cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post=cur.fetchall()
    # conn.commit()
    print(current_user.email)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int ,db: Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user) ):
    # cur.execute("""SELECT * FROM POSTS WHERE id=%s""",(str(id),))
    # post=cur.fetchone()
    post=db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="404error")
    return  post
    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int,db: Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post=cur.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id == id )

    if post_query.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")

    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post (id: int,post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title=%s ,content=%s,published=%s WHERE id =%s RETURNING *""",(post.title, post.content, post.published,str(id)))
    # updated_post=cur.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id== id)
    post=post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_query.update(post.dict(),synchroze_session=False)
    db.commit()
    return post_query.first()