FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies (curl for healthcheck)
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p /logs /recipes && \
    chmod -R 755 /logs /recipes

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    HOST=0.0.0.0 \
    PORT=6088 \
    WORKERS=2 \
    LOG_LEVEL=info \
    LOG_FILE_PATH=/logs/app.log

# Expose the port
EXPOSE 6088

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:${PORT:-6088}/api/health || exit 1

# Run the application
CMD ["python", "main.py"]