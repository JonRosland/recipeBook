# Frontend build stage
FROM node:lts AS frontend-builder
WORKDIR /app/frontend
COPY frontend/ . 
RUN npm install && npm run build

# Backend build stage
FROM python:3.8-slim AS backend-builder
WORKDIR /app/backend
#COPY backend/requirements.txt . 
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt
#COPY backend/ .

FROM alpine:latest
WORKDIR /app

# Install Node.js, npm, Python, pip, and any other system dependencies
RUN apk update
RUN apk add --no-cache nodejs npm python3 py3-pip 
# If there are specific build tools needed for npm packages, install them here
# For example, apk add --no-cache make g++ for packages that require native build tools

# Copy the built frontend and backend artifacts from their respective builder stages
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist
COPY /frontend/package.json /app/frontend
COPY --from=backend-builder /app/backend /app/backend

# Install Python and Node.js dependencies
#RUN python3 -m venv ~/pyvenv --system-site-packages
#RUN ~/pyvenv/bin/pip3 install -r /app/backend/requirements.txt

RUN pip3 install -r /app/backend/requirements.txt --break-system-packages
# Ensure you're in the right directory to run npm install for frontend dependencies
RUN pwd
RUN ls
RUN cd frontend/ && npm install 
RUN cd ..
RUN pwd
# Set any environment variables
ENV HOST=0.0.0.0
ENV PORT=4321
EXPOSE 4321
# Correct the CMD to run both services, as discussed previously
CMD sh -c "python3 /app/backend/main.py & node /app/frontend/dist/server/entry.mjs"