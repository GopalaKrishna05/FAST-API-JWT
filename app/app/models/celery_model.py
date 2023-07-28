from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.schemas.celery_schema import CeleryState

Base = declarative_base()


class CeleryWorkerStatus(Base):
    __tablename__ = "celery_worker_status"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    worker_name = Column(String(length=250))
    task_id = Column(String(length=250))
    # status = Column(Enum(CeleryState), default=CeleryState.ACTIVE.value, nullable=False)
    status = Column(String(50), Enum(CeleryState), default=CeleryState.ACTIVE.value, nullable=False)
    subscription_name = Column(String(length=250))
    topic_name = Column(String(length=250))
    mirror_topic_name = Column(String(length=250))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ttl_start_time = Column(DateTime, nullable=True, default=datetime.utcnow)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String(length=250))
    user_password = Column(String(length=250))