ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base
ENV PYTHONUNBUFFERED=1

WORKDIR /app/api
COPY . .
RUN python -m pip install -r requirements.txt
EXPOSE 8000
# ENV DJANGO_SUPERUSER_PASSWORD=1234
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]