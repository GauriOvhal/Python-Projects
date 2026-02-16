from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config  # Import DB URI from config.py

# Create SQLAlchemy engine using the URI from config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

