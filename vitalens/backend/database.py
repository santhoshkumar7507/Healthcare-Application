"""VitaLens — database.py"""
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime, uuid, os
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./vitalens.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PatientRecord(Base):
    __tablename__ = "patient_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_name = Column(String)
    disease = Column(String)
    risk_score = Column(Integer)
    confidence = Column(Float)
    city = Column(String)
    blockchain_tx = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="patient")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
