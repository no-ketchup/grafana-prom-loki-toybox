# Python runtime
FROM python:3.12-slim

# --- Runtime env tweaks ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# App directory
WORKDIR /opt/app

# Install Python deps
RUN pip install \
      "flask>=3.0,<4.0" \
      "prometheus-client>=0.20,<1.0" \
      "gunicorn>=21.2,<22.0"

# Copy source
COPY app.py ./

# Run as non-root
RUN useradd -u 1000 -r -s /usr/sbin/nologin appuser \
  && chown -R appuser:appuser /opt/app
USER appuser

EXPOSE 8000

# Logs to stdout, tunable workers/threads via env
ENV WORKERS=2 THREADS=2
CMD ["bash", "-lc", "gunicorn -b 0.0.0.0:8000 app:app --workers ${WORKERS} --threads ${THREADS} --access-logfile - --error-logfile -"]
