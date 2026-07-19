# Build stage: Vite SPA
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps 2>&1
COPY . .
RUN npm run build

# Runtime stage: FastAPI + static files
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and built frontend
COPY backend/ ./backend/
COPY --from=builder /app/dist/ ./static/

# Volume for SQLite persistence
VOLUME ["/data"]

ENV STATIC_DIR=/app/static
ENV LEADS_DB_PATH=/data/leads.db

EXPOSE 80

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
