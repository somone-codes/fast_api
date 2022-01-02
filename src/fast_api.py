import models
from database.alchemy_orm import engine
from routers import post, user, authentication

from fastapi import FastAPI

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)


@app.get("/")
def index():
    return "Hello!"
