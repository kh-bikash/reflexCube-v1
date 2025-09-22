# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ./requirements.txt /app/requirements.txt

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy local wheels if present
COPY ./wheels /wheels

# Install Python dependencies, use local wheels if they exist
RUN if [ -d "/wheels" ]; then \
        pip install --no-cache-dir -r requirements.txt --find-links /wheels ; \
    else \
        pip install --no-cache-dir -r requirements.txt ; \
    fi

# Copy the rest of the application
COPY . /app

# Initialize Git for DVC and MLflow
RUN git init
