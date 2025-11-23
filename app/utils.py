from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def make_password_hash(password: str):
#     return pwd_context.hash(password)
def make_password_hash(password: str) -> str:
    pwd = password.encode("utf-8")[:72]
    return pwd_context.hash(pwd.decode("utf-8", errors="ignore"))


def verify_password(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)