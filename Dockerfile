# Development stage using npm/vite dev server
FROM node:22-alpine as dev
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm ci
COPY ./shared ../shared
COPY ./frontend .
EXPOSE 5173 9229
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Production stage using npm serve instead of nginx
FROM node:22-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files
COPY ./frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy shared directory first
COPY ./shared ../shared

# Copy source code
COPY ./frontend .

# Build the application
RUN npm run build

# Production stage - serve with npm
FROM node:22-alpine

WORKDIR /app

# Install serve globally for serving static files
RUN npm install -g serve

# Copy built assets from builder stage
COPY --from=builder /app/dist ./dist

# Expose port 3000 (serve default port)
EXPOSE 3000

# Start serve
CMD ["serve", "-s", "dist", "-l", "3000"]