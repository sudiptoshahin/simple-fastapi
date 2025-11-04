from fastapi import FastAPI, Depends
# database models
from . import models
from .database import engine
from .routes import post, user, auth, vote

# db connection
models.Base.metadata.create_all(bind=engine)
print('___Database_connected____')

10.36.37

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



# path operations
@app.get('/')
async def root():
    return {'message': 'Hello World Message Api'}

