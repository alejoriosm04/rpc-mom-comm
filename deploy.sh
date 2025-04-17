#!/bin/bash

# Exit on error
set -e

echo "Building Docker images..."

# Build frontend
echo "Building ecommerce-front..."
docker build -t ecommerce-front:latest ./ecommerce-app

# Build API Gateway
echo "Building api-gateway..."
docker build -t api-gateway:latest ./api-gateway

# Build Product Service
echo "Building product_service..."
docker build -t product_service:latest ./microservices/product_service

# Build Inventory Service
echo "Building inventory_service..."
docker build -t inventory_service:latest ./microservices/inventory_service

# Build Order Service
echo "Building order_service..."
docker build -t order_service:latest ./microservices/order_service

echo "All images built successfully!"

# Deploy the stack
echo "Deploying stack..."
docker stack deploy -c docker-compose.yml ecommerce-app

echo "Stack deployed successfully!" 