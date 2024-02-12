from sqlalchemy import create_engine 
#This line imports the create_engine function from the SQLAlchemy library.
#create_engine is used to create a database engine, which manages connections 
#to the database.
from sqlalchemy.orm import sessionmaker
#This line imports the sessionmaker class from the SQLAlchemy ORM 
#(Object-Relational Mapping) module. sessionmaker is a factory function
# that creates new Session objects, which are used to interact with the database.
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
#url to the data base 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
