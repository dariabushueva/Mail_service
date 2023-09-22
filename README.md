# Проект Mail Service
Сервис по управлению рассылками, администрированию и получению статистики по выполненным рассылкам. Также реализовано приложение БЛОГ для продвижения сервиса.

# Запуск Mail Service
## 1. Клонирование репозитория
```commandline
git clone https://github.com/dariabushueva/Django_online_store.git
```
## 2. Установка зависимостей
Создать виртуальное окружение:
```commandline
python -m venv venv
```
Активировать виртуальное окружение:
```commandline
venv\Scripts\activate.bat  для Windows
source venv/bin/activate  для Linux и MacOS
```
Установить зависимости:
```commandline
pip install -r requirements.txt
```

## 3. Установка и запуск Redis
Установка:
```commandline
sudo apt-get install redis-server
```
Запуск:
```commandline
sudo service redis-server start
```

## 4. Установка и настройка PostgreSQL
Установка:
```commandline
sudo apt-get install postgresql
```
Запуск:
```commandline
psql -U postgres
```
Создание базы данных, где mail_service - название базы данных, которое можно изменить в файле .env
```commandline
CREATE DATABASE mail_service;
```
Закрыть PostgreSQL:
```commandline
\q
```
## 5. Настройка переменных окружения
В папке config/ создать файл .env, в который записать свои данные:
```commandline
SECRET_KEY=
PSQL_DB_NAME=mail_service
PSQL_USER=
PSQL_PASSWORD=
EMAIL_PORT=
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
CACHE_ENABLED=True
CACHES_LOCATION=redis://127.0.0.1:6379
```

## 6. Применение миграций
```commandline
python manage.py migrate
```

## 7. Наполнение базы данных. Все данные предоставлены только в качестве примера.
```commandline
python manage.py loaddata blog_data.json
python manage.py loaddata mailings_data.json
python manage.py loaddata user_data.json
```

## Запуск сервера Django
```commandline
python manage.py runserver
```

## Запуск сервиса периодических задач
```commandline
python manage.py updater 
```