# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 5173

# Set environment variable for API URL (browser accesses via localhost)
ENV VITE_API_BASE_URL=http://localhost:8000

# Start dev server (for production, use: npm run build && npm run preview)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
