from time import time
from psycopg2.extras import RealDictCursor
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1n33dApassword@localhost:5432/fastapiDB"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         connection = psycopg2.connect(
#             host="localhost",
#             database="fastapiDB",
#             user="postgres",
#             password="1n33dApassword",
#             cursor_factory=RealDictCursor
#         )
#         cursor = connection.cursor()
#         print("Connected to PostgreSQL")
#         break
#     except psycopg2.Error as e:
#         print(f"Error connecting to PostgreSQL: {e}")
#         time.sleep(2)