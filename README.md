# Celery_Redis
Учебный проект, демонстрирующий:
1. Клиент отправляет POST /jobs, а FastAPI создаёт задачу в Redis
2. FastAPI мгновенно возвращает job_id
3. Celery Worker забирает задачу из очереди
4. Worker выполняет time.sleep(2)
5. Worker сохраняет результат в Redis
6. Клиент опрашивает GET /jobs/{job_id} и получает статус и результат

# Структура проекта

CELERY_REDIS/

    main.py - FastAPI приложение (эндпоинты)
    tasks.py - Celery задачи (фоновая обработка)
    config.json - Пороги температур (cold_max, hot_min)
    requirements.txt - Python зависимости
    dockerfile - Docker образ
    .gitignore - Git ignore
    README.md - Документация

# Шаг 1 — поставить задачу в очередь
curl -s -X POST http://localhost:8000/jobs \
 -H "Content-Type: application/json" \
 -d '{"temperature": 35}' | python -m json.tool

Ожидаемый ответ:
{
 "job_id": "a1b2c3d4-...",
 "status": "queued"
}

Ответ: Ссылка на скрин https://imgbox.com/glamSeBs

# Шаг 2 — подождать 3 секунды и проверить результат
JOB_ID="<подставьте job_id из предыдущего ответа>"
sleep 3
curl -s http://localhost:8000/jobs/$JOB_ID | python -m json.tool

Ожидаемый ответ:
{
 "status": "done",
 "result": {
 "category": "hot",
 "temperature": 35.0
 }
}

Ответ: Ссылка на скрин https://imgbox.com/38uIgnaO
