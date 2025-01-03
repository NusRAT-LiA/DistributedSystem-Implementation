# # Frontend Dockerfile
# FROM node:18-alpine as build

# # Set working directory
# WORKDIR /frontend

# # Copy package.json and install dependencies
# COPY package.json package-lock.json ./
# RUN npm install

# # Copy app source and build
# COPY . .
# RUN npm run build

# # Serve with Nginx
# FROM nginx:alpine
# COPY --from=build /frontend/build /usr/share/nginx/html

# # Expose Nginx default port
# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
# Use the official Node.js image to build the app
FROM node:23-alpine AS build

# Set the working directory
WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the app for production
RUN npm run build

# Use an Nginx container to serve the frontend
FROM nginx:alpine

# Copy built files from the build stage
COPY --from=build /frontend/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
