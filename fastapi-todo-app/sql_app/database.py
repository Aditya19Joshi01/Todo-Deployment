import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read database URL from environment; fall back to local SQLite for dev/imports
DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///./todo_app.db"

# If using SQLite we need to set check_same_thread for SQLAlchemy
if DATABASE_URL.startswith("sqlite"):
	engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
	engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
