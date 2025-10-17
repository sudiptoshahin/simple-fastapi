from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# ALGORITHM
# expiration time

SECRET_KEY = "2392e3p2ke2p3okep23o0ek23023k2pko3e;2podjko23hfoinonwlkdfjwlkj"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUITES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUITES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
