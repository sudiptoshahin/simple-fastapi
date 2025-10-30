from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from .config import settings

# connection string
# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/simple-fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except OperationalError as err:
    print(f"_____________Database connection failed!______________", err)

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













# Database connection with psycopg2 adapter
#____RAW_SQL______
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='simple-fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('_________Database connection was successfull!__________')
#         break
#     except Exception as error:
#         print(f"Connecting to database failed! \nError: {error}")
#         time.sleep(2)
# End Database connection