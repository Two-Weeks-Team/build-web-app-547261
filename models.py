import os
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", "sqlite:///./app.db"))

if DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

connect_args = {}
if not DATABASE_URL.startswith("sqlite"):
    lowered = DATABASE_URL.lower()
    if "localhost" not in lowered and "127.0.0.1" not in lowered:
        connect_args = {"sslmode": "require"}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PlanningArtifact(Base):
    __tablename__ = "bwa_planning_artifacts"

    id = Integer()
    id = __import__("sqlalchemy").Column(Integer, primary_key=True, index=True)
    title = __import__("sqlalchemy").Column(String(200), nullable=False)
    raw_input = __import__("sqlalchemy").Column(Text, nullable=False)
    preferences_json = __import__("sqlalchemy").Column(Text, nullable=False, default="{}")
    summary = __import__("sqlalchemy").Column(Text, nullable=False)
    items_json = __import__("sqlalchemy").Column(Text, nullable=False)
    score = __import__("sqlalchemy").Column(Integer, nullable=False, default=70)
    is_fallback = __import__("sqlalchemy").Column(Boolean, default=False)
    note = __import__("sqlalchemy").Column(Text, nullable=True)
    created_at = __import__("sqlalchemy").Column(DateTime, default=datetime.utcnow)
    updated_at = __import__("sqlalchemy").Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    snapshots = relationship("ArtifactSnapshot", back_populates="artifact", cascade="all, delete-orphan")


class ArtifactSnapshot(Base):
    __tablename__ = "bwa_artifact_snapshots"

    id = __import__("sqlalchemy").Column(Integer, primary_key=True, index=True)
    artifact_id = __import__("sqlalchemy").Column(Integer, ForeignKey("bwa_planning_artifacts.id"), nullable=False)
    version = __import__("sqlalchemy").Column(Integer, nullable=False, default=1)
    summary = __import__("sqlalchemy").Column(Text, nullable=False)
    items_json = __import__("sqlalchemy").Column(Text, nullable=False)
    score = __import__("sqlalchemy").Column(Integer, nullable=False, default=70)
    note = __import__("sqlalchemy").Column(Text, nullable=True)
    created_at = __import__("sqlalchemy").Column(DateTime, default=datetime.utcnow)

    artifact = relationship("PlanningArtifact", back_populates="snapshots")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
