# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/

# Switch to backend folder
WORKDIR /app/backend

# Expose port (Render sets $PORT externally)
EXPOSE 8000

# Start FastAPI using Render's $PORT
CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
