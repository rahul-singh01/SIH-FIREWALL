# Dockerfile content for frontend/package.json

# Use a multi-stage build to reduce the image size
FROM node:18 AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package.json frontend/package-lock.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY frontend/ /app/

# Build the frontend
RUN npm run build

# Final stage
FROM nginx:alpine

# Copy the built files from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf