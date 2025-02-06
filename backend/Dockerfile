# Stage 1: Build Stage
# Using an official Python runtime as a parent image
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Stage 2: Production Stage
# Using a slim version of the official Python runtime as a parent image for the final stage
FROM python:3.9-slim

# Set environment variables (if any)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copy the rest of the application code from the builder stage
COPY --from=builder /app /app

# Make the manage.py executable
RUN chmod +x manage.py

# Expose the port the app runs on (if applicable)
# EXPOSE 8000

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]