# Build stage
FROM node:18-alpine AS builder

WORKDIR /usr/src/sveltekit

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /usr/src/sveltekit

# Add curl for healthcheck
RUN apk update && apk add curl

# Set environment variables
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=8080

# Copy built assets from builder stage
COPY --from=builder /usr/src/sveltekit/build ./build
COPY --from=builder /usr/src/sveltekit/package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# Create a non-root user and switch to it
RUN adduser -D svelteuser
USER svelteuser

# Expose the port the app runs on
EXPOSE 8080

# Start the application
CMD ["node", "build"]