# Build
FROM node:11.6.0-alpine AS builder
WORKDIR /app
COPY . /app
RUN npm i
RUN $(npm bin)/ng build

# Serve
FROM nginx:1.15.8-alpine
COPY --from=builder /app/dist/frontend/ /usr/share/nginx/html
