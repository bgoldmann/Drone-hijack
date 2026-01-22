# Docker Development Guide

Comprehensive guide for containerizing applications with Docker in Cursor IDE. Covers Dockerfiles, docker-compose, multi-stage builds, and best practices.

## Overview

Docker provides:
- **Containerization**: Package applications with dependencies
- **Consistency**: Same environment across dev/staging/production
- **Isolation**: Isolated environments for each service
- **Scalability**: Easy to scale and deploy

## Dockerfile Basics

### Node.js/Next.js Dockerfile

```dockerfile
# Base image
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build application
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### Python/FastAPI Dockerfile

```dockerfile
# Multi-stage build
FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Commands

### Building Images

```bash
# Build image
docker build -t myapp:latest .

# Build with tag
docker build -t myapp:v1.0.0 .

# Build from specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .
```

### Running Containers

```bash
# Run container
docker run -p 3000:3000 myapp:latest

# Run in detached mode
docker run -d -p 3000:3000 myapp:latest

# Run with environment variables
docker run -p 3000:3000 -e NODE_ENV=production myapp:latest

# Run with volume mount
docker run -p 3000:3000 -v $(pwd):/app myapp:latest

# Run with name
docker run --name myapp -p 3000:3000 myapp:latest
```

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# View logs
docker logs <container-id>
docker logs -f <container-id>  # Follow logs

# Execute command in container
docker exec -it <container-id> sh
```

## Docker Compose

### Basic docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Full Stack Example

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Build and start
docker-compose up --build

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# View logs
docker-compose logs
docker-compose logs -f app

# Execute command in service
docker-compose exec app sh
```

## Multi-Stage Builds

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
CMD ["npm", "start"]
```

## Best Practices

### 1. Use .dockerignore

```dockerignore
node_modules
npm-debug.log
.git
.gitignore
.env
.env.local
.next
dist
build
.DS_Store
*.md
```

### 2. Layer Caching

Order Dockerfile commands to maximize cache hits:

```dockerfile
# Dependencies change less often
COPY package.json package-lock.json ./
RUN npm ci

# Application code changes more often
COPY . .
RUN npm run build
```

### 3. Use Specific Tags

```dockerfile
# BAD - can change unexpectedly
FROM node:latest

# GOOD - specific version
FROM node:18-alpine
```

### 4. Non-Root User

```dockerfile
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs
```

### 5. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1
```

## Checklist for Docker

Before deploying:

- [ ] .dockerignore configured
- [ ] Multi-stage builds used (if applicable)
- [ ] Non-root user configured
- [ ] Environment variables from .env files
- [ ] Health checks configured
- [ ] Volumes for persistent data
- [ ] Ports correctly exposed
- [ ] Dependencies properly installed
- [ ] Images built and tested locally
