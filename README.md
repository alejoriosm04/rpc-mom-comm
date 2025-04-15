## RPC communication system with MOM failure system

Communication system between Remote Processes with MOM Failover Mechanism.

### Architecture Proposal

![image](https://github.com/user-attachments/assets/d8fd110f-116f-483d-8341-9d52f9809936)

### To-Do List

- [X] Implement the REST Client.
- [X] Implement the API Gateway.
- [X] Implement the RPC communication system.
- [X] Implement the microservice 1.
- [ ] Implement the microservice 2.
- [ ] Implement the microservice 3.
- [X] Implement the MOM Failover Mechanism.
- [ ] Create the documentation.

### 📁 Project structure

```
.
├── README.md
├── api-gateway/
├── db/
├── docker-compose.yml
├── docs/
├── ecommerce-app/ <--- REST Client (Next.js)
├── microservices/
└── mom/
```

#### 1. REST Client (Next.js)

At the moment, the REST Client is a simple Next.js application that uses the `fetch` API to make requests to the API Gateway.

First, add the following env variables to your `.env.local` file:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

To run the REST Client, you need to have Node.js installed. Then, you can run the following commands:

```bash
npm install
npm run dev
```

Otherwise, you can use the `docker-compose.yml` file to run the REST Client.

```bash
docker-compose up -d --build
```
Then, you can access the REST Client at `http://localhost:3000`.

**Note:** This is the same process to deploy the REST Client in AWS, remember to enable the `3000` port in the AWS Security Group.

---

### 2. API Gateway (FastAPI)

**Note:** Duplicate the pb folder in the api-gateway folder and add it in the product-service folder to avoid errors

The API Gateway is built with FastAPI and acts as the entry point for all requests. It communicates with the microservices using gRPC.

To run the API Gateway:

Add the following env variables to your .env file: 

```bash
PRODUCT_SERVER_HOST=localhost
PRODUCT_SERVER_PORT=50051
RABBITMQ_HOST=localhost
RABBITMQ_QUEUE=product_queue
RABBITMQ_URL=amqp://guest:guest@localhost/
```
Then: 

```bash
cd api-gateway
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload 
```

Then, access the documentation at:  
👉 `http://localhost:8000/docs`

> ℹ️ Make sure your microservices are running before calling the API Gateway.

---

### 3. Microservice 1 (Products Service - gRPC)

This microservice provides product data via gRPC. It must be running so the API Gateway can fetch data through it.

To run the microservice:

Add the following env variables to your .env file: 

**Note:** Do not forget to include `MONGODB_URL` in the .env file.

```bash
GRPC_SERVER_PORT=50051
DATABASE_NAME=ecommerce-db
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_URL=amqp://guest:guest@localhost/
QUEUE_NAME=product_requests
```
Then:

```bash
cd microservices/product_service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py  # or the main server file
```

> ✅ This will start the gRPC server that listens for product requests.

---

### 4. MOM Failover Mechanism (RabbitMQ)

To run the MOM Failover Mechanism:

```bash
# latest RabbitMQ 4.x
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

> ✅ This will start the RabbitMQ server that listens for product requests.

**Note:** If you want to try the failover mechanism, turn off the microservice, reload the `products` page in the Next.js application and turn on the microservice again.

---

