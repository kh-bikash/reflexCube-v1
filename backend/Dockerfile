# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# === NEW STEP: Copy the pre-downloaded wheels ===
COPY ./wheels /wheels

# Install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip

# === MODIFIED STEP: Use --find-links to point to the local wheels ===
RUN pip install --no-cache-dir -r requirements.txt --find-links /wheels

# Copy the rest of the application's code
COPY . /app

# Initialize Git for DVC
RUN git init
