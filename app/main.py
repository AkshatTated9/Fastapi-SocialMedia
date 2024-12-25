from fastapi import FastAPI
from .database import engine
from . import models
from .routers import  post,user,auth,vote

app=FastAPI()
# models.Base.metadata.create_all(bind=engine)      #allows sqlalchemy to create tables now of no use since alembic is used to create tables

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def default():
    return "Homepage"




