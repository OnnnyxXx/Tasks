FROM python:3.11-slim

WORKDIR /app


COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/


COPY wait-for-it.sh /app/

# Открываем порт для доступа
EXPOSE 8000

# Запускаем миграции и сервер разработки
CMD ["bash", "wait-for-it.sh", "db", "5432", "--", "bash", "-c", "python coolsite/manage.py migrate && python coolsite/manage.py runserver 0.0.0.0:8000"]