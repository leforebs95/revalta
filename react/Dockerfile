# Build stage
FROM node:18-alpine AS builder

WORKDIR /usr/src/react

# # Add curl for healthcheck
RUN apk update && apk add curl

# Expose the port the app runs on
EXPOSE 8080

# Copy package.json and package-lock.json
COPY package*.json ./

RUN npm ci

COPY . .


# Start the application
CMD [ "sh", "react-entry"]
