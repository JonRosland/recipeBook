#!/bin/bash
# Script to build and push Docker images to Docker Hub

# Configuration
DOCKER_USERNAME="jonro"  # Replace with your Docker Hub username
VERSION="1.0"                            # Change this to increment versions
IMAGE_PREFIX="recipebook"                  # Base name for your images

# Ensure Docker is logged in
echo "Logging in to Docker Hub..."
docker login

if [ $? -ne 0 ]; then
    echo "Error: Docker Hub login failed. Exiting."
    exit 1
fi

# Build images locally first, using docker-compose
echo "Building Docker images locally..."
docker compose build --no-cache

if [ $? -ne 0 ]; then
    echo "Error: Docker image build failed. Exiting."
    exit 1
fi

# Tag and push backend image
echo "Pushing backend image to Docker Hub..."
docker tag recipebook-backend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}
docker tag recipebook-backend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:latest
docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}
docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:latest

# Tag and push frontend image
echo "Pushing frontend image to Docker Hub..."
docker tag recipebook-frontend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}
docker tag recipebook-frontend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:latest
docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}
docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:latest

echo "Docker images successfully pushed to Docker Hub:"
echo "  - ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}"
echo "  - ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}"
echo "Done!"