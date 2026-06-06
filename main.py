import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Temperature Classifier")

CONFIG_PATH = Path(os.getenv("CONFIG_PATH", "config.json"))


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Config not found: {CONFIG_PATH}")
    with open(CONFIG_PATH) as f:
        return json.load(f)


class ClassifyRequest(BaseModel):
    temperature: float


class ClassifyResponse(BaseModel):
    category: str
    temperature: float


@app.post("/classify", response_model=ClassifyResponse)
def classify(request: ClassifyRequest):
    config = load_config()
    t = request.temperature
    if t < config["cold_max"]:
        category = "cold"
    elif t > config["hot_min"]:
        category = "hot"
    else:
        category = "comfortable"
    return ClassifyResponse(category=category, temperature=t)


@app.get("/health")
def health():
    
    return {"status": "ok"}


# TODO: добавить импорты для Celery
# from tasks import app as celery_app, run_inference

# TODO: добавить модели ответов
# class JobResponse(BaseModel): ...
# class JobResult(BaseModel): ...

# TODO: реализовать POST /jobs
# @app.post("/jobs", ...)
# def create_job(request: ClassifyRequest): ...

# TODO: реализовать GET /jobs/{job_id}
# @app.get("/jobs/{job_id}", ...)
# def get_job(job_id: str):
#     task = celery_app.AsyncResult(job_id)  # явная привязка к app, не AsyncResult из celery.result
#     ...
