from fastapi import FastAPI, Depends
# database models
from . import models
from .database import engine
from .routes import post, user, auth

# db connection
models.Base.metadata.create_all(bind=engine)
print('___Database_connected____')

# __8.43.16

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)




# path operations
@app.get('/')
async def root():
    return {'message': 'Hello World Message Api'}

