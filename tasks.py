from celery import Celery
import time

# TODO: создать Celery app с именем 'tasks'
# Укажите broker и backend — оба смотрят на Redis на localhost:6379
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',    # TODO: заполнено — проверьте, что Redis запущен
    backend='redis://localhost:6379/0'    # TODO: заполнено — нужен для хранения результатов
)


@app.task
def run_inference(payload: dict) -> dict:
    # TODO: добавить имитацию тяжёлой задачи
    # Подсказка: time.sleep(N) — «модель думает» N секунд
    pass  # TODO: удалить и написать реализацию

    # TODO: вернуть словарь с результатом
    # Пример: {"category": "hot", "temperature": 35.0}
