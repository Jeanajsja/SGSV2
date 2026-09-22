FROM python:3.11-slim
WORKDIR /app
COPY services/reservas/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY services/reservas/ ./
COPY shared ./shared
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
EXPOSE 5006
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5006", "app:app"]
