import requests
import time
import concurrent.futures

# Температуры для теста
temperatures = [10, 20, 35]

# запрос на создание задачи
def create_job(temp):

    response = requests.post(
        "http://localhost:8000/jobs",
        json={"temperature": temp}
    )
    data = response.json()
    print(f"Temperature {temp}°C → Job ID: {data['job_id']}")
    return data['job_id']

# статус задачи
def check_status(job_id):

    response = requests.get(f"http://localhost:8000/jobs/{job_id}")
    return response.json()

# Шаг 1: Создаём 3 задачи параллельно
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    job_ids = list(executor.map(create_job, temperatures))

print(f"\nВсе задачи созданы: {job_ids}")

# Шаг 2: Ждём 3 секунды (задачи выполняются 2 секунды)
print("\nОжидаем 3 секунды...")
time.sleep(3)

# Шаг 3: Проверяем статусы
print("\nСтатусы задач:")
for job_id in job_ids:
    status = check_status(job_id)
    print(f"Job {job_id[:8]}... - Status: {status['status']}, Result: {status['result']}")