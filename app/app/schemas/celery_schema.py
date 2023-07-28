from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class CeleryState(Enum):
    ACTIVE = "ACTIVE"
    ERROR = "ERROR"
    DELETED = "DELETED"


class CeleryWorkerSchema(BaseModel):
    worker_name: Optional[str] = Field(
        None, description='Celery worker name'
    )
    task_id: Optional[str] = Field(
        None, description='Celery worker taskid'
    )
    status: Optional[str] = Field(None, description='Celery worker status ex: (ACTIVE|STOPPED|DELETED)')
    subscription_name: str = Field(None, description='Topic Subscription name')
    topic_name: Optional[str] = Field(
        None, description='topic name'
    )
    mirror_topic_name: Optional[str] = Field(
        None, description='mirror topic name'
    )
    ttl_start_time: Optional[datetime] = Field(
        None, description='ttl_start_time'
    )


class User(BaseModel):
    user_name: str
    user_password: str


class Displayuser(BaseModel):
    user_name: str

    class Config:
        Orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: Optional[str] = None
