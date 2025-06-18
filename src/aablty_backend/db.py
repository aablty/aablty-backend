from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

# Database URL from environment or default to SQLite
DATABASE_URL = settings.DATABASE_URL

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={
                           "check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():

    from .models import Base
    Base.metadata.create_all(bind=engine)
