

from email.policy import HTTP
from multiprocessing import synchronize
from sqlite3 import Cursor
from string import ascii_uppercase
from typing import Optional,List
from urllib import response

from fastapi import FastAPI, HTTPException,Response,status,Depends
from fastapi.exception_handlers import http_exception_handler
from fastapi.params import Body

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine)



app = FastAPI()


    

while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='mypassword123',cursor_factory=RealDictCursor)
        cur=conn.cursor()
        print("connection to database succesfull")
        break
    except Exception as error:
        print ("unable to connect")
        print (error)
        time.sleep(2)

my_posts=[{"title":"title of the post1","content":"somthing1","id":1},{"title":"title of the post2","content":"somthing2","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index_post(id: int):
    for i , p in enumerate(my_posts):
        if p["id"]==id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World1"}





 