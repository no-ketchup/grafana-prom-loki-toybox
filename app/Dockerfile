FROM python:3.12-slim
WORKDIR /opt/app
COPY app.py .
RUN pip install flask prometheus-client gunicorn
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers", "2", "--threads", "2"]
