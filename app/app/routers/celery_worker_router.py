from fastapi.routing import APIRouter
from app.api.endpoints import celery_worker_service, user_service, login

celery_api_router = APIRouter()
celery_api_router.include_router(celery_worker_service.router, prefix='/celery_worker', tags=["Celery-Worker-Apis"])
celery_api_router.include_router(user_service.router, prefix='/user', tags=["User-Api"])
celery_api_router.include_router(login.router, tags=["Login-Api"])
