FROM python:3.11-slim

WORKDIR /app

COPY services/login/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/login/ ./
COPY shared ./shared

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
EXPOSE 5001

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5001", "app:app"]
