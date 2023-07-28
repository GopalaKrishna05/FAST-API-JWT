from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.celery_model import User as Users
from app.schemas.celery_schema import TokenData
# from app.config.log import logger
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/login')
def login(schema_info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.user_name == schema_info.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or Invalid User")
    if not pwd_context.verify(schema_info.password, user.user_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")

    access_token = generate_token(data={"sub": user.user_name})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid auth credentials',
                                         headers={"WWW-Authentication": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get('sub')
        if user_name is None:
            raise credential_exception
        TokenData(username=user_name)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": 401,
                    "message": "Request had invalid authentication credentials",
                    "status": "UNAUTHENTICATED",
                    "details": {
                        "type": "Auth error",
                        "reason": "ACCESS_TOKEN_TYPE_UNSUPPORTED"
                    }
                }
            }
        )
    except JWTError:
        raise credential_exception
    except Exception as e:
        raise e
