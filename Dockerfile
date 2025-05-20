# Dockerfile
FROM python:3.11

# Set working directory
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .