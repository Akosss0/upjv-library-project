# -- Part 1 - React
FROM node:22.22.0-alpine3.23 AS build
WORKDIR /app

# Install packages
COPY react/package*.json ./
RUN npm install

# Build project
COPY react/. .
RUN npm run build

# -- Part 2 - Proxy
FROM nginx:1.28.1
RUN rm -rf /usr/share/nginx/html/*
# Copy previously compiled project (part 1) into nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html
