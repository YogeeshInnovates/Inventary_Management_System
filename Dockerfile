

FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install system dependencies + Python packages
# RUN apt-get update && \
#     apt-get install -y netcat-openbsd && \
#     rm -rf /var/lib/apt/lists/* && \
#     pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/* && \
    pip install  --no-cache-dir -r requirements.txt


# Copy app and start script
COPY app ./app
COPY start.sh .
# Copy Alembic migration files
COPY alembic.ini .
COPY alembic ./alembic

# Make start.sh executable
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
