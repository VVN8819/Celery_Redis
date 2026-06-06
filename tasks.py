from celery import Celery
import time
import os
import json
from pathlib import Path

# TODO: создать Celery app с именем 'tasks'
# Укажите broker и backend — оба смотрят на Redis на localhost:6379
app = Celery(
    'tasks',
    broker='redis://redis-broker:6379/0',    # TODO: заполнено — проверьте, что Redis запущен
    backend='redis://redis-broker:6379/0',    # TODO: заполнено — нужен для хранения результатов
    broker_connection_retry_on_startup=True
)

CONFIG_PATH = Path(os.getenv("CONFIG_PATH", "config.json"))

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config not found: {CONFIG_PATH}")
    with open(CONFIG_PATH) as f:
        return json.load(f)


@app.task
def run_inference(payload: dict) -> dict:
    # TODO: добавить имитацию тяжёлой задачи
    time.sleep(2) # — «модель думает» 2 секунды
    
    t = payload["temperature"]
    
    config = load_config() # идем в config.json за данными
    
    if t < config["cold_max"]:
        category = "cold"
    elif t > config["hot_min"]:
        category = "hot"
    else:
        category = "comfortable"

    # TODO: вернуть словарь с результатом
    return {
        "category": category,
        "temperature": t
    }
