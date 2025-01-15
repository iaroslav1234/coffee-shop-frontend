FROM node:18-alpine

WORKDIR /app

# Copy package files first for better caching
COPY frontend/package*.json ./

# Install dependencies and serve
RUN npm install && \
    npm install -g serve

# Copy the rest of the code
COPY frontend/ ./

# Set production environment
ENV NODE_ENV=production
ENV CI=false

# Build the app
RUN npm run build

# Create start script
RUN echo '#!/bin/sh\nserve -s build --listen ${PORT:-3000}' > start.sh && \
    chmod +x start.sh

# Start the app
CMD ["./start.sh"]
