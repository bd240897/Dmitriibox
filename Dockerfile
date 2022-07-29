# образ на основе которого создаём контейнер
FROM python:3.8.6-alpine

# рабочая директория внутри проекта
# ВНИМЕНИЕ - МЫ копирвем ТУТ только ТЕ файлы рядом с которыми тусит DockerFile!!!!!!!!!!!!!!!
# т.е. в папке будет (пример) /usr/src/mysite/manage.py
WORKDIR /usr/src/Dmitriibox

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости для Postgre
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# копируем содержимое текущей папки в контейнер
COPY . .