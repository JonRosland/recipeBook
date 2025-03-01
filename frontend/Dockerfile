# Build stage
FROM denoland/deno:latest as builder

WORKDIR /app

# Install Node.js and Yarn - fixed to avoid the npx conflict
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy package files first to leverage caching
COPY package.json ./

# Create a Deno environment shim as CommonJS (.cjs) for build process
RUN echo 'globalThis.Deno = { env: { get: function(key) { return process.env[key] || ""; } } };' > deno-shim.cjs

# Copy lock files
COPY yarn.lock deno.lock ./

# Install dependencies with a clean slate
RUN yarn install

# Now copy the rest of the source code
COPY . .

# Set build environment variables
# URL for server-side API calls 
ENV SERVER_API_URL="http://backend:6088/api/"
# URL for client-side API calls
ENV PUBLIC_API_URL="http://localhost:6088/api/"
ENV PUBLIC_ENABLE_FAVORITES="true"
ENV PUBLIC_ENABLE_SEARCH="true"
ENV PUBLIC_THEME="light"
ENV PUBLIC_ITEMS_PER_PAGE="12"
ENV NODE_ENV="production"

# Build the application
RUN yarn build

# Runtime stage
FROM denoland/deno:latest

WORKDIR /app

# Copy built files from builder stage
COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/run-server.mjs ./

# Set environment variables
ENV PORT=${PORT:-8085}
# URL for server-side API calls
ENV SERVER_API_URL=${SERVER_API_URL:-http://backend:6088/api/}
# URL for client-side API calls
ENV PUBLIC_API_URL=${PUBLIC_API_URL:-http://localhost:6088/api/}
ENV PUBLIC_ENABLE_FAVORITES=${PUBLIC_ENABLE_FAVORITES:-true}
ENV PUBLIC_ENABLE_SEARCH=${PUBLIC_ENABLE_SEARCH:-true}
ENV PUBLIC_THEME=${PUBLIC_THEME:-light}
ENV PUBLIC_ITEMS_PER_PAGE=${PUBLIC_ITEMS_PER_PAGE:-12}
ENV BASE_PATH=${BASE_PATH:-/}

# Expose the port
EXPOSE ${PORT:-8085}

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8085}/ || exit 1

# Start the Deno server
CMD ["deno", "run", "--allow-net", "--allow-read", "--allow-env", "./run-server.mjs"]