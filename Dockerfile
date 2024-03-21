ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base
ENV PYTHONUNBUFFERED=1

WORKDIR /app/api
COPY . .
RUN python -m pip install -r requirements.txt
EXPOSE 8000
RUN python manage.py makemigrations
RUN python manage.py migrate 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

