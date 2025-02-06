# Dockerfile content for backend/manage.py

# Use a multi-stage build to reduce the image size
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY backend/requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY backend/ /app/

# Final stage
FROM python:3.11-slim

# Copy the dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Set the working directory
WORKDIR /app

# Copy the application code
COPY backend/ /app/

# Set the entrypoint to manage.py
ENTRYPOINT ["python", "manage.py"]