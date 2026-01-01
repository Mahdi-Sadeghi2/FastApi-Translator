import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read database connection string from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine (echo=True enables SQL query logging)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a database session factory
session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for SQLAlchemy models
BASE = declarative_base()


def get_db():
    """
    Dependency that provides a database session
    and ensures it is properly closed after use.
    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()
