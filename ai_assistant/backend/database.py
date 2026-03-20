import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import chromadb
from chromadb.config import Settings

# SQLite Setup
DB_DIR = os.path.join(os.getcwd(), "data")
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

SQL_DB_PATH = os.path.join(DB_DIR, "metadata.db")
engine = create_engine(f"sqlite:///{SQL_DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DocumentMetadata(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")

Base.metadata.create_all(bind=engine)

# ChromaDB Setup
CHROMA_PATH = os.path.join(DB_DIR, "chroma")
def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
