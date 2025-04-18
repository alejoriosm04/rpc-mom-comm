
# 🧩 RPC-MOM Communication System with Failover system

This project implements a communication system between distributed microservices using gRPC and RabbitMQ for MOM-based failover. It includes an API Gateway(FastAPI), a REST Client (Next.js), and microservices for products, inventory, and orders with real-time notifications.

---

## 📦 Architecture

![image](https://github.com/user-attachments/assets/d8fd110f-116f-483d-8341-9d52f9809936)

---

## ✅ Features

- gRPC communication between services
- RabbitMQ as MOM failover mechanism
- Queued processing when services are down
- Real-time feedback via WebSockets (orders and product updates)
- REST API Gateway with API Key authentication
- Rate limiting per endpoint
- MongoDB database for persistence
- Docker support for all services

---

## 📁 Project Structure

```
.
├── api-gateway/                 # FastAPI Gateway (gRPC + WebSocket + queue fallback)
├── ecommerce-app/              # Next.js Client (REST consumer)
├── microservices/
│   ├── product_service/
│   ├── inventory_service/
│   └── order_service/
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Environment Variables

### ✅ `api-gateway/.env`

```env
PRODUCT_SERVER_HOST=product_service
PRODUCT_SERVER_PORT=50051
RABBITMQ_HOST=rabbitmq
RABBITMQ_QUEUE=product_queue
RABBITMQ_URL=amqp://guest:guest@rabbitmq/
INVENTORY_SERVER_HOST=inventory_service
INVENTORY_SERVER_PORT=50052
ORDER_SERVER_HOST=order_service
ORDER_SERVER_PORT=50053
API_KEY=mysecretkey123
API_KEY_NAME=x-api-key

```

### ✅ `microservices/product_service/.env`

```env
GRPC_SERVER_PORT=50051
DATABASE_NAME=ecommerce-db
MONGODB_URL=url
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_URL=amqp://guest:guest@rabbitmq/
QUEUE_NAME=product_requests
API_GATEWAY_URL=http://api-gateway:8000
INVENTORY_SERVER_HOST=inventory_service
INVENTORY_SERVER_PORT=50052

```

### ✅ `microservices/inventory_service/.env`

```env
MONGODB_URL=url
DATABASE_NAME=ecommerce-db

RABBITMQ_URL=amqp://guest:guest@rabbitmq/
QUEUE_NAME=inventory_queue

INVENTORY_SERVER_HOST=inventory_service
INVENTORY_SERVER_PORT=50052

PRODUCT_SERVER_HOST=product_service
PRODUCT_SERVER_PORT=50051

ORDER_SERVER_HOST=order_service
ORDER_SERVER_PORT=50053

```

### ✅ `microservices/order_service/.env`

```env
GRPC_SERVER_PORT=50053

MONGODB_URL=url
DATABASE_NAME=ecommerce-db

RABBITMQ_URL=amqp://guest:guest@rabbitmq/
QUEUE_NAME=order_queue

API_GATEWAY_URL=http://api-gateway:8000

PRODUCT_SERVER_HOST=product_service
PRODUCT_SERVER_PORT=50051

INVENTORY_SERVER_HOST=inventory_service
INVENTORY_SERVER_PORT=50052 


```

### ✅ `ecommerce-app/.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_API_KEY=mysecretkey123  

```

---

## 🚀 Running the Project

### Step 1: Build and run all services

```bash
docker-compose up -d --build
```

### Step 2: Access the services

- **API Gateway** → [http://localhost:8000/docs](http://localhost:8000/docs)
- **Next.js Client** → [http://localhost:3000](http://localhost:3000)
- **RabbitMQ Dashboard** → [http://localhost:15672](http://localhost:15672)  

---

## 💡 Features Tested

### ✅ Real-time Orders (WebSocket)

- Orders show a message like `"Your order has been confirmed"` or `"Queued"` in real-time.
- If `order_service` is down, the request is queued and the client is notified.
- When `order_service` comes back, the order is processed and the client is notified via WebSocket.

### ✅ Real-time Product Updates

- The system listens for `/push/products` via WebSocket.
- When products are updated (stock changes), the UI reflects them automatically.

---

## 🔐 API Key Protection

All protected routes require the following header:

```
x-api-key: supersecretkey
```

This applies to:

- `/api/products/`
- `/api/orders/`
- `/api/inventory/check`

---

## 🧪 Testing Failover

1. Stop a microservice (e.g. `order_service`).
2. Make a request (e.g. Add to Cart).
3. You'll see a message like: `Order queued. Waiting for confirmation...`
4. Start `order_service` again:
   ```bash
   docker-compose up -d order_service
   ```
5. The client will receive real-time confirmation via WebSocket.

---

## 🧪 Manual Testing Summary

- ✅ The system was tested using Docker containers for all microservices (`product_service`, `order_service`, `inventory_service`, `api-gateway`, `rabbitmq`).
- ✅ The client (`ecommerce-app`) was run locally using `npm run dev` for development and WebSocket debugging purposes.

### 🔁 Run the frontend locally

```bash
cd ecommerce-app
npm install
npm run dev
```
