from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Log(Base):
    __tablename__ = 'api_log'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String)
    message = Column(Text)

class Policy(Base):
    __tablename__ = 'api_policy'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    action = Column(String)
    source_ip = Column(String)
    destination_ip = Column(String)
    protocol = Column(String)
    port = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Application(Base):
    __tablename__ = 'api_application'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    version = Column(String)
    is_active = Column(Boolean, default=True)

class Alert(Base):
    __tablename__ = 'api_alert'

    id = Column(Integer, primary_key=True)
    level = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)

# Database connection
def get_db_engine(config):
    return create_engine(config.DATABASE_URL)

# Create tables
def create_tables(engine):
    Base.metadata.create_all(engine)