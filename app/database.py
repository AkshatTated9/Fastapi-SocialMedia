from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor
from .config import settings


SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()



# for estabilishing connection with db for raw constructed tables in postgresql using psycopg2
# while True:
#     try:
#         conn=psycopg2.connect(host="localhost",dbname="Item_details",user="postgres",password="Navkar96",cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Connection Established")
#         break
#     except Exception as error:
#         print("Connection Failed")
#         print("Error:", error)
#         time.sleep(3)
