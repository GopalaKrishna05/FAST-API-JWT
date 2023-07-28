from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.crud.celery_crud import get_celery_workers, create_celery_workers, update_celery_worker, \
    partial_update_celery_worker, delete_celery_worker_by_subscription_name, get_user_by_subscription_name
from app.models import celery_model
from app.schemas.celery_schema import CeleryWorkerSchema
from app.database.session import engine, get_db
from app.schemas.celery_schema import User
from app.api.endpoints.login import get_current_user

celery_model.Base.metadata.create_all(bind=engine)

router = APIRouter()


# app = FastAPI(title="Kafka-Federation")


@router.post("/create", response_model=CeleryWorkerSchema)
def create_celery_worker(schema_info: CeleryWorkerSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(celery_model.CeleryWorkerStatus).filter(
        celery_model.CeleryWorkerStatus.subscription_name == schema_info.subscription_name).first()
    try:
        if db_user:
            return JSONResponse(status_code=404, content="User Already Existed")
        res = create_celery_workers(db=db, user=schema_info)
        user_json = jsonable_encoder(res)
        return JSONResponse(content=user_json, status_code=201)
    except Exception as er:
        return JSONResponse(content=str(er), status_code=500)


@router.get("/get_by_subscription_name/{subscription_name}")
def get_celery_worker_by_subscription(subscription_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    celery_worker_res = get_user_by_subscription_name(db, subscription_name)
    return celery_worker_res


@router.get("/")
def get_celery_worker(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    celery_worker_res = get_celery_workers(db)
    return celery_worker_res


@router.patch("/partial_update_by_subscription_name", response_model=CeleryWorkerSchema)
def partial_update_by_subscription_name(schema_info: CeleryWorkerSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        res = partial_update_celery_worker(db=db, schema_info=schema_info)
        user_json = jsonable_encoder(res)
        return JSONResponse(content=user_json, status_code=201)
    except Exception as er:
        return JSONResponse(content=str(er), status_code=500)


@router.put("/update_by_subscription_name", response_model=CeleryWorkerSchema)
def update_by_subscription_name(schema_info: CeleryWorkerSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        res = update_celery_worker(db=db, schema_info=schema_info)
        user_json = jsonable_encoder(res)
        return JSONResponse(content=user_json, status_code=201)
    except Exception as er:
        return JSONResponse(content=str(er), status_code=500)


@router.delete("/deleted_by_subscription_name/{subscription_name}")
def delete_celery_worker(subscription_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    celery_worker_res = delete_celery_worker_by_subscription_name(db, subscription_name)
    return celery_worker_res
