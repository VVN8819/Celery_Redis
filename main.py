import json
import os
from pathlib import Path
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# TODO: добавить импорты для Celery
from tasks import app as celery_app, run_inference

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


# 2. Добавить в main.py два эндпоинта
# TODO: добавить модели ответов
# Ответ при создании задачи
class JobResponse(BaseModel):
    job_id: str
    status: str

# Ответ при проверке статуса задачи
class JobResult(BaseModel):
    status: str
    result: dict

# TODO: реализовать POST /jobs
# Создаёт асинхронную задачу классификации
@app.post("/jobs", response_model=JobResponse)
def create_job(request: ClassifyRequest):
    payload = {"temperature": request.temperature}
    task = run_inference.delay(payload)
    
    return JobResponse(
        job_id=task.id,
        status="queued"
    )
    

# TODO: реализовать GET /jobs/{job_id}
# Проверяет статус задачи по job_id. Возвращает статус и результат
@app.get("/jobs/{job_id}", response_model=JobResult)
def get_job(job_id: str):
    task = celery_app.AsyncResult(job_id)  # явная привязка к app, не AsyncResult из celery.result

    if task.state == "PENDING":
        return JobResult(status="queued", result=None)
    
    elif task.state == "STARTED":
        return JobResult(status="started", result=None)
    
    elif task.state == "SUCCESS":
        return JobResult(status="done", result=task.result)
    
    elif task.state == "FAILURE":
        return JobResult(status="failed", result={"error": str(task.info)})
    
    else:
        return JobResult(status=task.state.lower(), result=None)
        

        
    
