# Pull base image
FROM python:3.8-slim as web

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# General Tools
RUN apt-get update && apt-get install -y \
        build-essential \
        netcat \
        libpq-dev \
        gcc \
        && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --upgrade pip
COPY requirements ./requirements
RUN pip install -r ./requirements/production.txt

# Copy all files
COPY . .
EXPOSE 8000
RUN ["chmod", "+x", "./entrypoints/entrypoint.sh"]

# Collect Static Files
RUN SECRET_KEY=foo python manage.py collectstatic --noinput --settings=weather.settings.production

ENTRYPOINT ["./entrypoints/entrypoint.sh"]
