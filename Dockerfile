ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app/api

COPY requirements.txt  .

RUN python -m pip install -r requirements.txt

COPY .  .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]