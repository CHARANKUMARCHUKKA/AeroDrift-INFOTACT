# AeroDrift Enterprise Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required for underlying libraries
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Security: Run as non-root user
RUN useradd -m aerodrift && chown -R aerodrift:aerodrift /app
USER aerodrift

# Default entrypoint starts the Cloud Topology Engine
EXPOSE 8000
# Default entrypoint starts the REST API server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
