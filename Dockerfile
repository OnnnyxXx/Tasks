FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ../coolsite ./coolsite


CMD ["python", "coolsite/manage.py", "runserver", "0.0.0.0:8000"]