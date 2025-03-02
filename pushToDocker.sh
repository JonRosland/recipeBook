#!/bin/bash
# Script to build and push Docker images to Docker Hub

# Configuration
DOCKER_USERNAME="jonro"      # Replace with your Docker Hub username
VERSION="1.2"                # Change this to increment versions
IMAGE_PREFIX="recipebook"    # Base name for your images

# Ensure Docker is logged in
echo "Logging in to Docker Hub..."
docker login
if [ $? -ne 0 ]; then
    echo "Error: Docker Hub login failed. Exiting."
    exit 1
fi

# Ask the user which image(s) to push
echo "Which image do you want to push to Docker Hub?"
echo "1) Frontend"
echo "2) Backend"
echo "3) Both"
read -p "Enter your choice (1, 2, or 3): " choice

# Build images based on the user's choice
case "$choice" in
    1)
        echo "Building Docker image for frontend..."
        docker compose build frontend --no-cache
        if [ $? -ne 0 ]; then
            echo "Error: Docker image build failed. Exiting."
            exit 1
        fi
        ;;
    2)
        echo "Building Docker image for backend..."
        docker compose build backend --no-cache
        if [ $? -ne 0 ]; then
            echo "Error: Docker image build failed. Exiting."
            exit 1
        fi
        ;;
    3)
        echo "Building Docker images for both frontend and backend..."
        docker compose build recipebook-backend recipebook-frontend --no-cache
        if [ $? -ne 0 ]; then
            echo "Error: Docker image build failed. Exiting."
            exit 1
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Push images based on the user's choice
case "$choice" in
    1)
        echo "Pushing frontend image to Docker Hub..."
        docker tag recipebook-frontend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}
        docker tag recipebook-frontend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:latest
        docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}
        docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:latest
        echo "Frontend image successfully pushed: ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}"
        ;;
    2)
        echo "Pushing backend image to Docker Hub..."
        docker tag recipebook-backend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}
        docker tag recipebook-backend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:latest
        docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}
        docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:latest
        echo "Backend image successfully pushed: ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}"
        ;;
    3)
        echo "Pushing backend image to Docker Hub..."
        docker tag recipebook-backend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}
        docker tag recipebook-backend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:latest
        docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}
        docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:latest

        echo "Pushing frontend image to Docker Hub..."
        docker tag recipebook-frontend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}
        docker tag recipebook-frontend:latest ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:latest
        docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}
        docker push ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:latest

        echo "Docker images successfully pushed to Docker Hub:"
        echo "  - ${DOCKER_USERNAME}/${IMAGE_PREFIX}-backend:${VERSION}"
        echo "  - ${DOCKER_USERNAME}/${IMAGE_PREFIX}-frontend:${VERSION}"
        ;;
esac

echo "Done!"
