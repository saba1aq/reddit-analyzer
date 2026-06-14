FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    xvfb \
    fonts-liberation \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

RUN SB_DRIVERS="$(python -c 'import seleniumbase, os; print(os.path.join(os.path.dirname(seleniumbase.__file__), "drivers"))')" \
    && mkdir -p "$SB_DRIVERS" \
    && cp /usr/bin/chromedriver "$SB_DRIVERS/uc_driver" \
    && chmod +x "$SB_DRIVERS/uc_driver"

COPY backend /app/backend

CMD ["celery", "-A", "src.infrastructure.tasks.celery_app", "worker", "--pool=solo", "--loglevel=info"]
