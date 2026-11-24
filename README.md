```markdown
# Умный дом: Микросервисная архитектура (ЛР6)

Проект состоит из двух FastAPI-сервисов (`api-gateway` и `storage`) и базы данных PostgreSQL. Приложение упаковано в Docker-контейнеры, настроен автоматический конвейер CI на GitHub Actions.

## Архитектура
- **api-gateway** (порт 8000) — шлюз для взаимодействия с клиентами.
- **storage** (порт 8001) — сервис хранения данных.
- **db** — база данных PostgreSQL 16 (порт 5432).

## Запуск приложения через Docker Compose

1. Создайте файл с переменными окружения на основе шаблона:
   ```bash
   cp .env.example .env
   ```

2. Соберите образы и запустите контейнеры в фоновом режиме:
   ```bash
   docker compose up --build -d
   ```

3. Дождитесь, пока все сервисы пройдут healthcheck (обычно 10-15 секунд). Проверить статус можно командой:
   ```bash
   docker compose ps
   ```
   *Все три контейнера (`db`, `storage`, `api-gateway`) должны иметь статус `healthy` или `running`.*

## Проверка доступности (Healthcheck)

Для проверки работоспособности сервисов выполните:
```bash
# Проверка API Gateway
curl http://localhost:8000/health

# Проверка Storage
curl http://localhost:8001/health
```
Оба сервиса должны вернуть JSON: `{"status":"ok"}`.

## Локальный запуск проверок и тестов

Для запуска тестов без Docker выполните следующие шаги из корня проекта:

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Установите зависимости (включая dev-инструменты):
   ```bash
   pip install -r storage/requirements.txt
   pip install -r api-gateway/requirements.txt
   pip install ruff mypy pytest
   ```

3. Запустите линтер, проверку типов и тесты:
   ```bash
   # Линтинг
   ruff check storage api-gateway

   # Проверка типов
   mypy storage/app api-gateway/app

   # Запуск тестов (по очереди, чтобы избежать конфликта имен модулей)
   cd storage && pytest && cd ..
   cd api-gateway && pytest && cd ..
   ```

## CI/CD (GitHub Actions)

Файл `.github/workflows/ci.yml` настраивает автоматический конвейер при каждом `push` в ветку `main`:
1. Поднимает чистую базу данных PostgreSQL.
2. Проверяет код линтером `ruff`.
3. Проверяет типы с помощью `mypy`.
4. Запускает тесты `pytest` (с передачей переменных окружения).
5. Выполняет сборку Docker-образов (`docker build`) для обоих сервисов.
```
```
