from sqlalchemy import create_engine 
#This line imports the create_engine function from the SQLAlchemy library.
#create_engine is used to create a database engine, which manages connections 
#to the database.
from sqlalchemy.orm import sessionmaker
#This line imports the sessionmaker class from the SQLAlchemy ORM 
#(Object-Relational Mapping) module. sessionmaker is a factory function
# that creates new Session objects, which are used to interact with the database.
from sqlalchemy.ext.declarative import declarative_base
#declarative functions 
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
#url to the data base 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#This line creates a database engine using the create_engine function.
# It takes the database URL (SQLALCHEMY_DATABASE_URL) as its first argument 
#and an optional connect_args parameter to specify additional connection arguments.
# In this case, it sets check_same_thread to False, which is required when using SQLite
# with multiple threads.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#This line creates a sessionmaker object named SessionLocal. It takes several parameters:

#autocommit=False: This disables autocommit mode for sessions created by this sessionmaker.
# In autocommit mode, each database operation is automatically committed.
#autoflush=False: This disables autoflush mode for sessions created by this sessionmaker. 
#Autoflush automatically flushes pending changes to the database before executing queries.
#This binds the sessionmaker to the database engine created earlier (engine), 
#so that sessions created by this sessionmaker will use that engine to connect 
#to the database.
Base = declarative_base()
#This line creates a base class for declarative class definitions using 
#the declarative_base 
#function. The resulting Base object is used as a base class for all ORM class definitions.
# It provides common functionality such as table creation and reflection.
