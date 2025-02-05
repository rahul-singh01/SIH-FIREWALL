# Dockerfile for frontend

# Stage 1: Build the frontend application
FROM node:18 AS build

WORKDIR /app

COPY frontend/package.json ./
COPY frontend/package-lock.json ./

RUN npm install

COPY frontend/ ./

RUN npm run build

# Stage 2: Serve the built application
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]