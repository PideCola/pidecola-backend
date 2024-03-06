ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .
RUN python -m pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py migrate 
CMD python manage.py runserver