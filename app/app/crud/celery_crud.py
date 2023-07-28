from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.config.log import logger
from app.models.celery_model import CeleryWorkerStatus
from app.schemas.celery_schema import CeleryWorkerSchema


def notfound_record():
    return {"message": "Record Not found"}


def successfully():
    return {"message": "Record deleted successfully"}


def create_celery_workers(db: Session, user: CeleryWorkerSchema):
    db_user = CeleryWorkerStatus(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_subscription_name(db: Session, subscription_name: str):
    celery_obj = db.query(CeleryWorkerStatus).filter(
        CeleryWorkerStatus.subscription_name == subscription_name).first()
    try:
        if celery_obj:
            return celery_obj
        else:
            return JSONResponse(content=notfound_record(), status_code=400)
    except Exception as err:
        return JSONResponse(content=str(err), status_code=500)


def get_celery_workers(db: Session):
    celery_obj = db.query(CeleryWorkerStatus).all()
    try:
        if celery_obj:
            return celery_obj
        else:
            return JSONResponse(content=notfound_record(), status_code=400)
    except Exception as err:
        return JSONResponse(content=str(err), status_code=500)


def partial_update_celery_worker(db: Session, schema_info: CeleryWorkerSchema):
    try:
        worker_model = db.query(CeleryWorkerStatus).filter(
            CeleryWorkerStatus.subscription_name == schema_info.subscription_name).first()
        if worker_model:
            worker_data = schema_info.model_dump(exclude_unset=True)
            for key, value in worker_data.items():
                setattr(worker_model, key, value)
            db.add(worker_model)
            db.commit()
            db.refresh(worker_model)
            return worker_model
        else:
            return JSONResponse(notfound_record(), 400)
    except Exception as err:
        logger.exception('OOPS somthing wrong')
        raise HTTPException(status_code=500, detail=str(err))


def update_celery_worker(db: Session, schema_info: CeleryWorkerSchema):
    try:
        worker_model = db.query(CeleryWorkerStatus).filter(
            CeleryWorkerStatus.subscription_name == schema_info.subscription_name).first()
        if worker_model:
            worker_data = schema_info.model_dump(exclude_unset=True)
            for key, value in worker_data.items():
                setattr(worker_model, key, value)
            db.add(worker_model)
            db.commit()
            db.refresh(worker_model)
            return worker_model
        else:
            return JSONResponse(notfound_record(), 400)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


def delete_celery_worker_by_subscription_name(db: Session, subscription_name: str):
    celery_obj = db.query(CeleryWorkerStatus).filter(
        CeleryWorkerStatus.subscription_name == subscription_name).first()
    try:
        if celery_obj:
            db.delete(celery_obj)
            db.commit()
            return JSONResponse(content=successfully(), status_code=200)
        else:
            return JSONResponse(content=notfound_record(), status_code=400)
    except Exception as err:
        return JSONResponse(content=str(err), status_code=500)
