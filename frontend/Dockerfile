# Étape 1 : build
FROM node:20 AS build

WORKDIR /app
COPY react/package.json react/package-lock.json ./
RUN npm install
COPY react/. .
RUN npm run build

# Étape 2 : serveur statique
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
