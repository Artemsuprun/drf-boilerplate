# syntax=docker/dockerfile:1
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=config.settings.prod \
    WEB_CONCURRENCY=2 \
    APP_HOME=/home/app/backend

WORKDIR ${APP_HOME}

# Create a non-root application user
RUN addgroup --system app && \
    adduser --system --ingroup app --home /home/app app && \
    mkdir -p ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles && \
    chown -R app:app /home/app

# Install dependencies first for better build caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY --chown=app:app . .

USER app

EXPOSE 8000

# Production default. Worker count comes from WEB_CONCURRENCY (read natively by gunicorn).
# --worker-tmp-dir /dev/shm avoids heartbeat stalls on container overlay filesystems.
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--worker-tmp-dir", "/dev/shm", \
     "--timeout", "60", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
