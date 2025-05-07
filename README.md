# **Skillfactory Virtual Traineeship**


**Описание**

Асинхронный веб-сервис на FastAPI для регистрации и управления информацией о горных перевалах.

Используется PostgreSQL, SQLAlchemy 2.0, Pydantic, Alembic.

Проект реализует REST API для создания, просмотра, поиска и редактирования перевалов

с привязкой к пользователям, координатам, уровням сложности и изображениями.


**Основные возможности**

Добавление нового перевала с вложенными данными (пользователь, координаты, уровни сложности, изображения).

Получение информации о перевале по ID.

Поиск всех перевалов, добавленных пользователем (по email).

Редактирование перевала (если статус позволяет).

Асинхронная работа с базой данных PostgreSQL.


**Стэк**

Python 3.10+

FastAPI

SQLAlchemy 2.0 (async)

PostgreSQL

Alembic

Pydantic

dotenv


**Структура проекта**

```
Skillfactory_Virtual_Traineeship/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── pereval.py
│   │   └── schemas/
│   │       └── pereval.py
│   ├── core/
│   │   └── config.py
│   └── db/
│       ├── repositories/
│       │   └── pereval.py
│       ├── databases.py
│       └── models.py
├── alembic/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```


**Пример входных данных для метода создания перевала**
json
```
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22 13:18:13",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Иванов",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {"data": "<картинка1>", "title": "Седловина"},
    {"data": "<картинка2>", "title": "Подъём"}
  ]
}
```


**Примеры вызова REST API с хостинга (Yandex Cloud)**

Базовый адрес API:
http://158.160.1.109:8000

Интерактивная документация:

Swagger UI: http://158.160.1.109:8000/docs

ReDoc:http://158.160.1.109:8000/redoc

1. Добавление нового перевала:
```
POST /submit_data
```

Пример запроса:
bash
```
curl -X POST "http://158.160.1.109:8000/submit_data/" \
  -H "Content-Type: application/json" \
  -d '{
    "beauty_title": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "add_time": "2021-09-22 13:18:13",
    "user": {
      "email": "qwerty@mail.ru",
      "fam": "Иванов",
      "name": "Василий",
      "otc": "Иванович",
      "phone": "+7 555 55 55"
    },
    "coords": {
      "latitude": "45.3842",
      "longitude": "7.1525",
      "height": "1200"
    },
    "level": {
      "winter": "",
      "summer": "1А",
      "autumn": "1А",
      "spring": ""
    },
    "images": [
      {"data": "<base64-строка>", "title": "Седловина"},
      {"data": "<base64-строка>", "title": "Подъём"}
    ]
  }'
```

Пример успешного ответа:
json
```
{
  "status": 200,
  "message": None,
  "id": 42
}
```

Пример ответа при ошибке SQLAlchemy:
json
```
{
  "status": 500,
  "message": f"Ошибка подключения к базе данных: {log ошибки}",
  "id": None
}
```

2. Получение информации о перевале по ID:
```
GET /submit_data/{id}
```

Пример запроса:
bash
```
curl "http://158.160.1.109:8000/submit_data/42/"
```

Пример успешного ответа:
json
```
{
  "id": 42,
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22T13:18:13",
  "status": "NEW",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Иванов",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
  "coords": {
    "latitude": 45.3842,
    "longitude": 7.1525,
    "height": 1200
  },
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {"title": "Седловина", "data": "<base64-строка>"},
    {"title": "Подъём", "data": "<base64-строка>"}
  ]
}
```

Пример ответа, если перевал не найден:
json
```
{
  "status": 404,
  "message": f"Перевал с id 999 в базе отсутствует."
}
```

3. Получение всех перевалов пользователя по email:
```
GET /submit_data/?user__email=<email>
```

Пример запроса:
bash
```
curl "http://158.160.1.109:8000/submit_data/?user_email=qwerty@mail.ru"
```

Пример успешного ответа:
json
```
[
  {
    "id": 42,
    "beauty_title": "пер. ",
    "title": "Пхия",
    "add_time": "2021-09-22T13:18:13",
    "status": "NEW",
    "coords": {
      "latitude": 45.3842,
      "longitude": 7.1525,
      "height": 1200
    },
    "level": {
      "winter": "",
      "summer": "1А",
      "autumn": "1А",
      "spring": ""
    },
    "images": [
      {"title": "Седловина", "data": "<base64-строка>"},
      {"title": "Подъём", "data": "<base64-строка>"}
    ]
  },
  {
    "id": 43,
    "beauty_title": "пер. ",
    "title": "Северный",
    "add_time": "2021-09-25T10:00:00",
    "status": "NEW",
    "coords": {
      "latitude": 45.4000,
      "longitude": 7.2000,
      "height": 1300
    },
    "level": {
      "winter": "",
      "summer": "1Б",
      "autumn": "1Б",
      "spring": ""
    },
    "images": []
  }
]
```

Пример ответа, если пользователь не найден:
json
```
{
  "status": 404,
  "message": "Пользователь с таким email не найден."
}
```

4. Редактирование перевала:
```
PATCH /submit_data/{id}/
```

Пример запроса:
bash
```
curl -X PATCH "http://158.160.1.109:8000/submit_data/{id}/42/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Пхия (обновлено)",
    "level": {
      "summer": "1Б",
      "autumn": "1Б"
    }
  }'
```

Пример успешного ответа:
json
```
{
  "state": 1,
  "message": None
}
```

Пример ответа, если редактирование запрещено:
json
```
{
  "state": 0,
  "message": "Редактирование невозможно. Текущий статус 'Принят'. Для редактирования должен быть статус 'Ожидает модерации'."
}
```

Пример ответа, если перевал не найден:
json
```
{
  "state": 404,
  "message": "Перевал не найден."
}
```

**Установка и запуск**

1. Клонируйте репозиторий:
bash

git clone https://github.com/Anton-otom/Skillfactory_Virtual_Traineeship.git

cd Skillfactory_Virtual_Traineeship

2. Создайте и активируйте виртуальное окружение:
bash
python -m venv .venv

Windows:
.\.venv\Scripts\activate

Linux/macOS:
source .venv/bin/activate

3. Установите зависимости:
bash
pip install -r requirements.txt

4. Настройте переменные окружения в файле .env. Пример содержимого:

FSTR_DB_HOST=localhost

FSTR_DB_PORT=5432

FSTR_DB_LOGIN=your_db_user

FSTR_DB_PASS=your_db_password

FSTR_DB_NAME=your_db_name

5. Примените миграции базы данных:
bash
alembic upgrade head

6. Запустите приложение:
bash
uvicorn main:app --reload


**Документация API:**

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc


**Контакты**

По вопросам и предложениям: an.vaseko@mail.ru