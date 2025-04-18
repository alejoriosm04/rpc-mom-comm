#!/bin/bash

# Exit on error
set -e

echo "Building Docker images..."

# Build frontend
echo "Building ecommerce-front..."
docker build -t ecommerce-front ./ecommerce-app

# Build API Gateway
echo "Building api-gateway..."
docker build -t api-gateway ./api-gateway

# Build Product Service
echo "Building product_service..."
docker build -t product_service ./microservices/product_service

# Build Inventory Service
echo "Building inventory_service..."
docker build -t inventory_service ./microservices/inventory_service

# Build Order Service
echo "Building order_service..."
docker build -t order_service ./microservices/order_service

echo "All images built successfully!"

# Deploy the stack
echo "Deploying stack..."
docker stack deploy -c docker-stack.yml ecommerce-app

echo "Stack deployed successfully!" 