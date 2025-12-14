from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# For development: using SQLite
DATABASE_URL = "sqlite:///./complaints.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for DB session (used in routers)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
