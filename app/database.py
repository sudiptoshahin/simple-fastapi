from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# connection string
# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/simple-fastapi'

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except OperationalError as err:
    print(f"Database connection failed!", err)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# database orm dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# end database orm dependecy