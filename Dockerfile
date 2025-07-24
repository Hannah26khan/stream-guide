# Use official Python image with security patches
FROM python:3.10-slim-bookworm

# Prevent Python from writing .pyc files & buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System package install (single clean step)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Expose port
EXPOSE 8080

# Start the app
CMD ["gunicorn", "-b", ":8080", "app:app"]

