from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os



load_dotenv(".env") 

database_hostname: str = os.getenv("DATABASE_HOSTNAME")
database_port: str = (os.getenv("DATABASE_PORT"))
database_password: str = os.getenv("DATABASE_PASSWORD")
database_username: str = os.getenv("DATABASE_USERNAME")
database_name: str = os.getenv("DATABASE_NAME")

#URL = 'postgresql://<username>:<password>@hostname:port><database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}'

#establish connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#talk to DB you need a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#this allows you to import this class by models, you inherit table making methods
Base = declarative_base()


#function to get a session to db, after request is done it closes.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()