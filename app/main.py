from fastapi import FastAPI
from . import models # . means curr directory
from .database import engine, get_db
from .routers import post, sqlAlchemyPost, user, auth
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password: str = "localhost"
    database_username: str = "postgres"
    secret_key: str = "shhhh"

settings = Settings()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db() 

app.include_router(post.router) #says to include these routes for http requests
app.include_router(sqlAlchemyPost.router)
app.include_router(user.router)
app.include_router(auth.router)

# my_posts = [{"title": "t1", "content": "c1", "id": 1}, {"title": "t2", "content": "c2", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_post_index(id):
#     for i, p in enumerate(my_posts): # lets you loop through a list with index + value, like forEach((val, index)) in JS.
#         if p['id'] == id:
#             return i




