# Dockerfile content for agent/main.py

# Use a multi-stage build to reduce the image size
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY agent/requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY agent/ /app/

# Final stage
FROM python:3.11-slim

# Copy the dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Set the working directory
WORKDIR /app

# Copy the application code
COPY agent/ /app/

# Set the entrypoint to main.py
ENTRYPOINT ["python", "main.py"]