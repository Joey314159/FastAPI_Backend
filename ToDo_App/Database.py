from sqlalchemy import create_engine

"""
        create_engine is the starting point for any SQLAlchemy application. It establishes the connection to our database
        and acts as the central source of connections throughout the app. Without it, SQLAlchemy has no way to communicate
        with the database.
"""
from sqlalchemy.orm import sessionmaker

"""
        sessionmaker creates a factory for generating database sessions. Each session acts as a workspace for 
        database operations and tracks all changes until they are committed or rolled back. We use it to interact 
        with the database in a controlled and isolated way.
"""

from sqlalchemy.ext.declarative import declarative_base

"""
        declarative_base creates a base class that all of our database table models will inherit from. By inheriting
        from Base, SQL_ALCHEMY recognizes a python class as a database table rather than a regular class. It is the 
        blueprint manager that connects our python models to the actual structure of the database
"""
SQL_ALCHEMY_URL = "sqlite:///./todos.db"
"""
        The reason why we are putting to check_same_thread to be false is because by default SQL Lite only allows one 
        thread to communicate with the data base. The reason SQL Lite does this is to prevent any kind of accident sharing 
        of the same connetion for different kind of requests. However in FastAPI it is very normal to have more than one 
        thread that can interact with the database at the same time which is why we want it to set it to false
"""
engine = create_engine(SQL_ALCHEMY_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""Base is the instance of declarative_base, all table modles in our app will inherit from the object"""
Base = declarative_base()
