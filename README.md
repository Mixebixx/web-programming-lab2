````md
# Lab 2 — REST API для управления задачами

REST API сервис для управления задачами, разработанный с использованием **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic** и **Docker**.

---

## Описание проекта

Приложение предоставляет CRUD API для работы с задачами.

Поддерживаются следующие операции:

- создание задачи
- получение списка задач
- получение задачи по ID
- полное обновление
- частичное обновление
- мягкое удаление (soft delete)

Удалённые задачи не отображаются в запросах получения.

---

## Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker / Docker Compose
- Pydantic

---

## Структура проекта

```text
lab2/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── utils/
│
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
````

---

## Переменные окружения

Создайте файл `.env` на основе `.env.example`.

Пример `.env.example`:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/tasks_db
```

---

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone <repository_url>
cd lab2
```

---

### 2. Запуск через Docker

```bash
docker-compose up --build
```

После запуска API будет доступно по адресу:

```text
http://localhost:4200
```

Swagger UI:

```text
http://localhost:4200/docs
```

---

## Миграции

Применение миграций:

```bash
docker-compose exec app alembic upgrade head
```

Создание новой миграции:

```bash
docker-compose exec app alembic revision --autogenerate -m "migration_name"
```

---

## API Endpoints

### Получить список задач

```http
GET /tasks
```

Параметры пагинации:

| Параметр | Тип | Описание                       |
| -------- | --- | ------------------------------ |
| page     | int | номер страницы                 |
| limit    | int | количество записей на странице |

Пример:

```http
GET /tasks?page=1&limit=10
```

---

### Получить задачу по ID

```http
GET /tasks/{task_id}
```

---

### Создать задачу

```http
POST /tasks
```

Пример тела запроса:

```json
{
  "title": "Первая задача",
  "description": "Проверка API",
  "status": "new"
}
```

---

### Полное обновление

```http
PUT /tasks/{task_id}
```

---

### Частичное обновление

```http
PATCH /tasks/{task_id}
```

---

### Удаление (soft delete)

```http
DELETE /tasks/{task_id}
```

Удаление является **мягким** — запись не удаляется из БД, а помечается временем удаления.

---

## Особенности реализации

* реализована модульная структура проекта
* используется soft delete через поле `deleted_at`
* реализована пагинация
* валидация входных данных через Pydantic
* миграции через Alembic
* конфигурация через `.env`

---

## Проверка функциональности

Поддерживаются все 6 HTTP методов:

* GET
* POST
* PUT
* PATCH
* DELETE
* GET by id

---

## Автор

Лабораторная работа №2 по дисциплине **Веб-программирование**.

Тема: разработка REST API сервиса с использованием FastAPI, PostgreSQL, Docker и Alembic.