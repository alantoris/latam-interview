# Dockerfile
FROM python:3.11

# Set working directory
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose the expected port
EXPOSE 8080

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Usamos el script como comando de arranque
CMD ["/start.sh"]
