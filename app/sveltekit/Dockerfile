# Build stage
FROM node:18-alpine AS builder

WORKDIR /usr/src/sveltekit

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN if [ "$PROD" = true ]; then npm ci --production; else npm ci; fi

COPY . .

RUN if [ "$PROD" = true ]; then npm run build; fi
RUN npm run build

# # Add curl for healthcheck
RUN apk update && apk add curl

# Create a non-root user and switch to it
RUN adduser -D svelteuser && chown -R svelteuser /usr/src/sveltekit
USER svelteuser

# Expose the port the app runs on
EXPOSE 8080

# Start the application
CMD if [ "$PROD" = true ]; then node build; else npm run dev -- --host ${HOST} --port ${PORT}; fi
