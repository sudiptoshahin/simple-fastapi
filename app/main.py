from fastapi import FastAPI, Depends
# database models
from . import models
from .database import engine
from .routes import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# db connection
models.Base.metadata.create_all(bind=engine)
print('___Database_connected____')

13.10.42

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



# path operations
@app.get('/')
async def root():
    return {'message': 'Hello World Message Api'}

