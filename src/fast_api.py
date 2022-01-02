import models
from database.alchemy_orm import engine
from routers import post

from fastapi import FastAPI

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)


@app.get("/")
def index():
    return "Hello!"
