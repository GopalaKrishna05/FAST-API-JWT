from sqlalchemy.orm import Session
from app.config.log import logger
from app.schemas.celery_schema import User
from app.models.celery_model import User as Users
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: User):
    hashed_pwd = pwd_context.hash(user.user_password)
    db_user = Users(user_name=user.user_name, user_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info('User created successfully')
    return db_user
