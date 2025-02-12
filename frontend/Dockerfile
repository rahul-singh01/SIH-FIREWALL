# Dockerfile for frontend

# Stage 1: Build the application
FROM node:14 AS builder

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY frontend/package.json frontend/package-lock.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY frontend/ /app/

# Build the application
RUN npm run build

# Stage 2: Production image
FROM nginx:alpine

# Copy the built application from the builder stage
COPY --from=builder /app/dist/ /usr/share/nginx/html/

# Expose the port the app runs on
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]