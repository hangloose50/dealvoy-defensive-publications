# app/db.py

import db.py
from app.sqlalchemy import create_engine
from app.sqlalchemy.ext.declarative import declarative_base
from app.sqlalchemy.orm import sessionmaker

# Load from .env or fallback to SQLite for easy dev
DB_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")

# Create engine (disable check_same_thread only for SQLite)
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

