#!/bin/bash

# Script to set up environment for the recipe application
# Usage: ./setup_environment.sh [development|production]

# Default to development environment
ENV_TYPE=${1:-development}
ENV_FILE=".env.${ENV_TYPE}"
TARGET_ENV=".env"

echo "Setting up ${ENV_TYPE} environment..."

# Check if the environment file exists
if [ ! -f "${ENV_FILE}" ]; then
    echo "Error: Environment file ${ENV_FILE} not found!"
    exit 1
fi

# Copy the environment file to .env
cp "${ENV_FILE}" "${TARGET_ENV}"
echo "Environment file ${ENV_FILE} copied to ${TARGET_ENV}"

# Create necessary directories
mkdir -p logs
mkdir -p recipes
echo "Created necessary directories"

# Set appropriate permissions
chmod 755 logs
chmod 755 recipes
echo "Set directory permissions"

# Additional setup for production
if [ "${ENV_TYPE}" = "production" ]; then
    # Check for required environment variables
    if [ -z "${SECRET_KEY}" ]; then
        # Generate a random secret key if not set
        export SECRET_KEY=$(openssl rand -hex 32)
        echo "Generated random SECRET_KEY"
    fi
    
    # Use environment variables to replace placeholders in .env
    # Replace placeholders in the .env file with actual environment variables
    sed -i "s/\${SECRET_KEY}/${SECRET_KEY}/g" "${TARGET_ENV}"
    sed -i "s/\${MONGODB_USER}/${MONGODB_USER:-root}/g" "${TARGET_ENV}"
    sed -i "s/\${MONGODB_PASSWORD}/${MONGODB_PASSWORD:-root}/g" "${TARGET_ENV}"
    sed -i "s/\${CORS_ALLOWED_ORIGINS}/${CORS_ALLOWED_ORIGINS:-*}/g" "${TARGET_ENV}"
    
    echo "Replaced environment variables in ${TARGET_ENV}"
fi

echo "Environment setup complete for ${ENV_TYPE} mode."
echo "You can now start the application with:"
echo "  python main.py"
echo "or with Docker:"
echo "  docker-compose up -d"