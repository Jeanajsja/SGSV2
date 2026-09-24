FROM python:3.11-slim
WORKDIR /app
COPY services/docentes/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY services/docentes/ ./
COPY shared ./shared
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
EXPOSE 5003
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5003", "app:app"]
