# CLI генератор Pydantic моделей и REST API контроллеров
## Установка
```bash
git clone https://github.com/SeregaSil/json-cli-rest
cd json-cli-rest
pip install -r requirements.txt
```
Необходимо создать в корне проекта файл окружения (*.env*) со следующими полями:
```env
POSTGRES_USER=<имя пользователя базы данных>
POSTGRES_PASSWORD=<пароль пользователя базы данных>
POSTGRES_HOST=<сервер базы данных>
POSTGRES_PORT=<порт сервера базы данных>
POSTGRES_DB=<имя базы данных>
```
Для миграции базы данных нужно выполнить следующую команду:
```bash
alembic upgrade head
```
## Возможности CLI
- ### Генерация Pydantic моделей на основе JSON Schema
```bash
python cli/cli.py gen-model --json-schema=<файл json-схемы>
```
Опции:
- *\-\-out-dir/-o* --- директория, в которую будет сохранена Pydantic модель (по умолчанию: ./rest/models)
- *\-\-name* --- задать место модели
- ### Генерация REST API контроллеров на основе Pydantic модели
```bash
python cli/cli.py gen-rest
```
Опции:
- *\-\-models/-m* --- директория c Pydantic моделями (по умолчанию: ./rest/models))
- *\-\-rest-routers/-r* --- директория, в которую будут сохранены REST API контроллеры (по умолчанию: ./rest/routers)
- ### Фиксирование изменений в git и добавление git tag
```bash
python cli/cli.py save <версия>
```
Опции:
- *\-\-message/-m* --- описание git commit (по умолчанию: '')
## REST API
Для запуска сервера:
```bash
uvicorn rest.app:app
```
Сервер будет запущен на localhost на порту 8000. Для запуска на другом хосту/порту можно использовать опцию *\-\-host/\-\-port*. Дополнительные опции можно посмотреть на оффициальном сайте [Uvicorn](https://www.uvicorn.org). По адресу *http[]()://host:port/docs* можно увидеть Swagger API, сгенерированный FastAPI.
## Файловая структура
```bash
└───json-cli-rest
    │   .gitignore
    │   alembic.ini
    │   config.py # Конфигурация проекта (значения задаются в .env)
    │   README.MD
    │   requirements.txt # Зависимости проекта
    ├───cli # Каталог CLI-составляющей проекта
    │   │   cli.py # Основной файл CLI
    │   │   generator.py # Файл с функциями генераторами кода
    │   ├───schemas
    │   │       custom-schema.json
    │   ├───templates # Jinja шаблоны для генерации кода
    │   │       model.jinja
    │   │       router.jinja
    │   └───__pycache__
    │           generator.cpython-311.pyc
    ├───migrations # Каталог alembic
    │   │   env.py
    │   │   README
    │   │   script.py.mako
    │   ├───versions
    │           2424741ec810_database_creation.py
    │
    ├───rest # Каталог REST API-составляющей проекта
    │   │   app.py # Основной файл REST API
    │   │   database.py # Файл с настройками подключения к базе данных
    │   │   db_model.py # Модель базы данных
    │   │
    │   ├───models # Каталог с сгенерированными Pydantic моделями
    │   │        custom_schema.py
    │   │
    │   ├───routers # Каталог с сгенерированными REST контроллерами
    │           custom_schema.py
```
## Исользуемые технологии
- [FastAPI](https://fastapi.tiangolo.com)
- [Pydantic](https://docs.pydantic.dev/1.10/)
- [click](https://click.palletsprojects.com/en/8.1.x/)
- [Jinja2](https://jinja.palletsprojects.com/en/2.9.x/intro/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://postgrespro.ru/docs/postgresql/15/intro-whatis)