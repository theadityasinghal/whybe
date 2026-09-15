FROM python:3.11-slim

WORKDIR /app

ENV MPLCONFIGDIR=/tmp/mpl_cache
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./server/
COPY source/ ./source/
COPY client/ ./client/

EXPOSE 8000

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
