# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the gRPC port
EXPOSE 50051

# Set environment variables
ENV GRPC_SERVER_PORT=50051
ENV DATABASE_NAME=ecommerce-db

# Run the application
CMD ["python", "main.py"] 