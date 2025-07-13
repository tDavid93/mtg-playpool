# Development stage
FROM node:18-alpine as development

WORKDIR /app

# Copy package files
COPY mtg-playpool-frontend/package*.json ./

# Install all dependencies (including devDependencies)
RUN npm ci --silent

# Copy source code
COPY mtg-playpool-frontend/ ./

# Expose port
EXPOSE 3000

# Development command
CMD ["npm", "start"]

# Production build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY mtg-playpool-frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production --silent

# Copy source code
COPY mtg-playpool-frontend/ ./

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine as production

# Copy built app to nginx
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]