"""
Database layer for MarketinAI standalone backend.
Uses SQLite for leads, orders and trial accounts.
"""
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data"))
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(DATA_DIR, 'marketinai.db')}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    service = Column(String, default="marketinai")
    nombre = Column(String)
    telefono = Column(String)
    empresa = Column(String)
    web = Column(String)
    vertical = Column(String)
    mensaje = Column(Text)
    extras = Column(Text)
    consent_rgpd = Column(Boolean, default=False)
    consent_marketing = Column(Boolean, default=False)
    source = Column(String, default="marketinai")
    funnel = Column(String, default="trial")
    url = Column(String)
    tags = Column(Text)
    metadata_json = Column(Text)
    utm_source = Column(String)
    utm_medium = Column(String)
    utm_campaign = Column(String)
    utm_content = Column(String)
    utm_term = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    tier = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="EUR")
    status = Column(String, default="pending")  # pending, paid, cancelled
    stripe_session_id = Column(String)
    stripe_payment_intent = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    paid_at = Column(DateTime)


class TrialAccount(Base):
    __tablename__ = "trial_accounts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    account_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4())[:12])
    plan = Column(String, default="starter")
    trial_days = Column(Integer, default=14)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime)
    converted = Column(Boolean, default=False)
    cancelled = Column(Boolean, default=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
