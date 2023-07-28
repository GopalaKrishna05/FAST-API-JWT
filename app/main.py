import uvicorn

from app.app.routers.celery_worker_router import celery_api_router
from fastapi import FastAPI, responses

app = FastAPI()

app.include_router(celery_api_router)


@app.get("/")
async def redirect_to_docs():
    return responses.RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
