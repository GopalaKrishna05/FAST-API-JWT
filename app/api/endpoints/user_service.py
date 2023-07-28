from fastapi import Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
# from app.crud.user import create_user
from app.database.session import get_db
from app.schemas.celery_schema import User, Displayuser
from app.config.log import logger
from app.models.celery_model import User as Users
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/create", response_model=Displayuser)
def create_users(schema_info: User, db: Session = Depends(get_db)):
    logger.info('Inside create user api')
    db_user = db.query(Users).filter(
        Users.user_name == schema_info.user_name).first()
    logger.info(f'checking db_user existed or not {db_user}')
    try:
        if db_user:
            return JSONResponse(status_code=404, content="User Already Existed")
        logger.info('User not Existed')
        hashed_pwd = pwd_context.hash(schema_info.user_password)
        create_new_user = Users(user_name=schema_info.user_name, user_password=hashed_pwd)
        db.add(create_new_user)
        db.commit()
        db.refresh(create_new_user)
        user_json = jsonable_encoder(create_new_user)
        user_data = {key: value for key, value in user_json.items() if key != "user_password"}
        logger.info('User created successfully')
        return JSONResponse(content=user_data, status_code=201)
    except Exception as er:
        return JSONResponse(content=str(er), status_code=500)
