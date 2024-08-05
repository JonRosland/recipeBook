# Stage 1: Build Backend
FROM python:3.13.0b4-slim AS backend-builder
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend .

# Stage 2: Build Frontend
FROM node:lts AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend .
RUN npm run build

# Stage 3: Production Image
FROM python:3.13.0b4-slim AS runtime

# Install Node.js to run the frontend
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend from the backend-builder stage
COPY --from=backend-builder /app/backend /app/backend

# Ensure the Python dependencies are included
COPY --from=backend-builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Copy frontend build output from the frontend-builder stage
COPY --from=frontend-builder /app/frontend /app/frontend

# Install only production dependencies for the frontend
WORKDIR /app/frontend
RUN npm install --production


# Expose the ports
EXPOSE 4000
EXPOSE 4321

# Define the command to run both backend and frontend
WORKDIR /app
CMD ["sh", "-c", "python3 /app/backend/main.py & node /app/frontend/dist/server/entry.mjs"]
