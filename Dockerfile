# Dockerfile for local dev + image processing support
FROM python:3.12-slim

# Prevent .pyc files & stream logs directly
env PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# 1. Install system-level dependencies
#    libpq-dev, gcc for psycopg
#    libjpeg-dev, zlib1g-dev for Pillow support
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libpq-dev gcc \
      libjpeg-dev zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# 2. Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy project code
COPY . .

# 4. Expose Django port
EXPOSE 8000

# 5. Entrypoint: run migrations then dev server
ENTRYPOINT ["sh","-c","\
  python manage.py makemigrations --noinput && \
  python manage.py migrate --noinput && \
  python manage.py collectstatic --noinput && \
  python manage.py runserver 0.0.0.0:8000\
"]