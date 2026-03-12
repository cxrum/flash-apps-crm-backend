from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.sqlalchemy_database_uri, pool_pre_ping=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#TODO Review the method of creating connection pools 
# and create basic abstaract class for creating sessions 
# for differnt pools (async and sycn). Also create an
# async worker pool for heavy queries.

def get_db() -> Generator[Session, None, None]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

