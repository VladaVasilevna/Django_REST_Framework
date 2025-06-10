# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Открываем порт 8000 для Django
EXPOSE 8000

# По умолчанию запускается Django сервер
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
