# Use the official Node.js image as the base image for building the project
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json package-lock.json ./

# Install npm dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the project files
COPY . .

# Build the Astro project
RUN npm run build

# Use the official Deno image as the base image for running the project
FROM denoland/deno:alpine-1.45.2 AS runtime

EXPOSE 8085

WORKDIR /app

# Copy the built project files from the build stage
COPY --from=build /app/dist /app/dist

# Run the server with necessary permissions
CMD ["deno", "run", "--allow-net", "--allow-read", "--allow-env", "./dist/server/entry.mjs"]
