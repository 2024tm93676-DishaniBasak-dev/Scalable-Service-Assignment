# -------------------------------
# Dockerfile for Rider Service
# -------------------------------

# Base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy project files into the container
COPY . /app

# create logs dir
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose the application port (5001)
EXPOSE 5001

# Set entrypoint to the script
CMD ["/app/entrypoint.sh"]
